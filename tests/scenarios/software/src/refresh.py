"""Example refresh command used as scenario evidence."""

import argparse
import json
from pathlib import Path


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the example cache.")
    parser.add_argument("--config", default="config/service.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = load_config(Path(args.config))
    print(f"retry_limit={config['retry_limit']} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
