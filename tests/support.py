"""Shared helpers for ai-docs-kit integration tests.

These helpers create disposable Git repositories, invoke real tools with argument
lists, and compare file inventories. They are test glue only: they do not install,
render, or validate anything on the toolkit's behalf.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"

ANSWERS_FILE = ".copier-answers.ai-docs-kit.yml"
DEFAULT_DOCS_DIR = "docs/ai-docs"
DEFAULT_REF = "v0.1.0"

# Pinned CI provisioning of the validation binary. These values are shared by the
# maintainer workflow, the inert consumer example, and their tests.
LYCHEE_VERSION = "0.24.2"
LYCHEE_ARCHIVE = "lychee-x86_64-unknown-linux-gnu.tar.gz"
LYCHEE_SHA256 = (
    "1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a"
)

WORKFLOW_EXAMPLE_START = "<!-- ai-docs-kit:workflow-example:start -->"
WORKFLOW_EXAMPLE_END = "<!-- ai-docs-kit:workflow-example:end -->"

# Never copy these into a template snapshot or a consumer fixture.
SNAPSHOT_IGNORE = shutil.ignore_patterns(
    ".git",
    ".venv",
    ".tools",
    "__pycache__",
    "*.py[cod]",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
)

# Consumer inventory produced by the MVP template, ordered for readable diffs.
EXPECTED_CONSUMER_INVENTORY = (
    ".ai-docs/README.md",
    ".ai-docs/lychee.toml",
    ".ai-docs/markdownlint-cli2.jsonc",
    ".ai-docs/policy.md",
    ".ai-docs/pre-commit-config.yaml",
    ".ai-docs/project.md",
    ".ai-docs/assets/adr.md",
    ".ai-docs/assets/document.md",
    ".ai-docs/assets/review.md",
    ".ai-docs/examples/AGENTS.snippet.md",
    ".ai-docs/examples/github-actions.md",
    ".ai-docs/skills/README.md",
    ".ai-docs/skills/docs-discover/SKILL.md",
    ".ai-docs/skills/docs-review/SKILL.md",
    ".ai-docs/skills/docs-write/SKILL.md",
    ".copier-answers.ai-docs-kit.yml",
    "docs/ai-docs/README.md",
    "docs/ai-docs/how-to/update-documentation.md",
    "docs/ai-docs/reference/documentation-policy.md",
)

CHECK_COMMAND = (
    "pre-commit",
    "run",
    "--config",
    ".ai-docs/pre-commit-config.yaml",
    "--all-files",
)


class MissingToolError(RuntimeError):
    """A required external tool is not available on PATH."""


def require_tool(name: str) -> str:
    """Return the absolute path of a required tool or fail with a clear message."""
    found = shutil.which(name)
    if not found:
        raise MissingToolError(
            f"Required tool '{name}' was not found on PATH. Provision the pinned "
            "maintainer toolchain from docs/maintainer-setup.md; integration tests "
            "must fail, not skip, when a required tool is missing."
        )
    return found


def tool_versions() -> dict[str, str]:
    """Collect exact versions of the tools used by the suite."""
    commands = {
        "copier": ("copier", "--version"),
        "pre-commit": ("pre-commit", "--version"),
        "node": ("node", "--version"),
        "markdownlint-cli2": ("markdownlint-cli2", "--version"),
        "lychee": ("lychee", "--version"),
        "skills-ref": ("skills-ref", "--version"),
        "git": ("git", "--version"),
    }
    versions = {}
    for label, command in commands.items():
        require_tool(command[0])
        result = run(list(command), check=True, timeout=120)
        versions[label] = result.stdout.strip().splitlines()[0]
    return versions


def run(
    command,
    cwd=None,
    *,
    check=True,
    timeout=600,
    stdin_text=None,
    env=None,
    extra_env=None,
):
    """Run a command without a shell and return the completed process.

    Failures include the command, exit code, and captured output so CI logs are
    actionable. Timeouts are bounded so a stuck tool cannot hang the suite.
    """
    command = [str(part) for part in command]
    merged_env = os.environ.copy()
    # Keep the developer's global/system Git configuration and prompts out of tests.
    merged_env.setdefault("GIT_CONFIG_NOSYSTEM", "1")
    merged_env.setdefault("GIT_CONFIG_GLOBAL", os.devnull)
    merged_env.setdefault("GIT_TERMINAL_PROMPT", "0")
    if env is not None:
        merged_env = dict(env)
    if extra_env:
        merged_env.update(extra_env)
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=merged_env,
            check=False,
        )
    except FileNotFoundError as error:
        raise MissingToolError(f"Command not found: {command[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Command timed out after {timeout}s: {' '.join(command)}"
        ) from error
    if check and result.returncode != 0:
        raise AssertionError(
            "Command failed with exit code "
            f"{result.returncode}: {' '.join(command)}\n"
            f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
        )
    return result



def git(repo, *args, check=True, timeout=300):
    """Invoke git in a repository, using only local identity setup by the tests."""
    return run(["git", *args], cwd=repo, check=check, timeout=timeout)


def init_repo(path) -> Path:
    """Create a Git repository with local-only identity and a quiet branch name."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q")
    git(path, "config", "--local", "user.name", "ai-docs-kit tests")
    git(path, "config", "--local", "user.email", "tests@example.invalid")
    git(path, "config", "--local", "commit.gpgsign", "false")
    git(path, "config", "--local", "init.defaultBranch", "main")
    return path


def commit_all(repo, message: str) -> str:
    """Stage and commit everything, returning the commit SHA."""
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message, "--no-verify")
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def tag(repo, name: str) -> None:
    git(repo, "tag", "-f", name)


def snapshot_template(destination, *, ref: str = DEFAULT_REF) -> Path:
    """Copy the working template into a disposable Git repo and tag it.

    Only repository content is copied; caches, virtual environments, the source
    repository's history, hooks, and remotes are excluded. The source repository is
    never tagged or committed by this helper.

    File modes are normalised to 0644 because the maintainer checkout may live on a
    filesystem without Unix mode bits (for example an NTFS mount). The published Git
    tree stores non-executable content as 0644, so a normalised snapshot matches what
    a consumer receives from a real clone.
    """
    destination = Path(destination)
    shutil.copytree(REPO_ROOT, destination, ignore=SNAPSHOT_IGNORE)
    for directory, _dirnames, filenames in os.walk(destination):
        os.chmod(directory, 0o755)
        for filename in filenames:
            os.chmod(Path(directory) / filename, 0o644)
    init_repo(destination)
    commit_all(destination, f"ai-docs-kit snapshot {ref}")
    tag(destination, ref)
    return destination


def copy_fixture(fixture_name: str, destination) -> Path:
    """Copy a checked-in fixture tree into a destination path."""
    destination = Path(destination)
    shutil.copytree(FIXTURES / fixture_name, destination)
    return destination


def render_project(
    template_repo,
    destination,
    *,
    docs_dir=None,
    project_name=None,
    ref: str = DEFAULT_REF,
    answers_file: str = ANSWERS_FILE,
    extra_args=(),
    check: bool = True,
    stdin_text=None,
):
    """Run the real Copier CLI with explicit arguments and no trust flag."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    command = [
        require_tool("copier"),
        "copy",
        "--defaults",
        "--vcs-ref",
        ref,
        "--answers-file",
        answers_file,
    ]
    if project_name is not None:
        command += ["--data", f"project_name={project_name}"]
    if docs_dir is not None:
        command += ["--data", f"docs_dir={docs_dir}"]
    command += list(extra_args)
    command += [str(template_repo), "."]
    return run(
        command,
        cwd=destination,
        check=check,
        stdin_text=stdin_text,
        timeout=600,
    )


def update_project(
    destination,
    *,
    ref: str,
    answers_file: str = ANSWERS_FILE,
    extra_args=(),
    check: bool = True,
    stdin_text=None,
):
    """Run `copier update` for the dedicated answers file."""
    command = [
        require_tool("copier"),
        "update",
        "--defaults",
        "--vcs-ref",
        ref,
        "--answers-file",
        answers_file,
    ]
    command += list(extra_args)
    return run(
        command,
        cwd=Path(destination),
        check=check,
        stdin_text=stdin_text,
        timeout=600,
    )


def run_checks(project, *, check=True, env=None):
    """Run the exact standalone pre-commit entry point over all scoped Markdown."""
    return run(
        list(CHECK_COMMAND),
        cwd=Path(project),
        check=check,
        env=env,
        timeout=600,
    )



def tree_hashes(root, *, exclude_prefixes=(".git",)) -> dict[str, str]:
    """Hash every regular file under `root` by POSIX relative path."""
    root = Path(root)
    hashes = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root).as_posix()
        if any(
            relative == prefix or relative.startswith(prefix + "/")
            for prefix in exclude_prefixes
        ):
            continue
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def file_hashes(root, paths) -> dict[str, str]:
    """Hash a named set of files, failing when one is missing."""
    root = Path(root)
    return {
        path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths
    }


def inventory(root, *, exclude_prefixes=(".git",)) -> list[str]:
    """List regular files relative to `root`, excluding VCS and cache paths."""
    return sorted(tree_hashes(root, exclude_prefixes=exclude_prefixes))


def conflict_files(root) -> list[str]:
    """Return files that still contain Git conflict markers."""
    root = Path(root)
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines = text.splitlines()
        if any(line.startswith("<<<<<<<") for line in lines) and any(
            line.startswith(">>>>>>>") for line in lines
        ):
            found.append(path.relative_to(root).as_posix())
    return found


def unmerged_paths(repo) -> list[str]:
    """Return paths Git still reports as unmerged in the index."""
    result = run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        cwd=Path(repo),
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def read_fenced_block(path, start_marker: str, end_marker: str) -> str:
    """Extract the raw text between two HTML-comment markers in a Markdown file."""
    text = Path(path).read_text(encoding="utf-8")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


def find_step(workflow: dict, name: str) -> dict:
    """Return the single workflow step with the given name."""
    steps = [
        step
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if step.get("name") == name
    ]
    if len(steps) != 1:
        raise AssertionError(f"expected exactly one step named {name!r}, got {steps!r}")
    return steps[0]


def workflow_from_example(path) -> dict:
    """Parse the YAML workflow embedded in the inert consumer example."""
    import yaml

    block = read_fenced_block(path, WORKFLOW_EXAMPLE_START, WORKFLOW_EXAMPLE_END).strip()
    if not block.startswith("```yaml"):
        raise AssertionError("the workflow example must be a fenced yaml block")
    body = block[len("```yaml") :].strip()
    if body.endswith("```"):
        body = body[: -len("```")].rstrip()
    return yaml.safe_load(body)


def write(path, text: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
