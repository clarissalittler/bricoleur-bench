import argparse
import sys
from pathlib import Path

import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a todo")
    add.add_argument("title")

    sub.add_parser("list", help="List todos")

    done = sub.add_parser("done", help="Mark a todo complete")
    done.add_argument("id", type=int)

    return parser


def main(argv: list[str]) -> int:
    _args = build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
