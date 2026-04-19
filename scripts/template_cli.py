#!/usr/bin/env python
"""Generic CLI example for the Python template."""

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="Generic CLI scaffold for this template")
    parser.add_argument("--name", default="world", help="Name to include in the output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    payload = {"message": f"Hello, {args.name}!", "tool": "python-template"}

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["message"])


if __name__ == "__main__":
    main()
