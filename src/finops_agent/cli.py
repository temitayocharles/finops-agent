from __future__ import annotations

import argparse
import json
import sys

from .io import analyze_file


def main() -> int:
    parser = argparse.ArgumentParser(prog="finops-agent", description="Kubernetes FinOps cost intelligence agent")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a FinOps evidence payload")
    analyze.add_argument("path", help="Path to an input JSON file")
    args = parser.parse_args()
    try:
        print(json.dumps(analyze_file(args.path), indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
