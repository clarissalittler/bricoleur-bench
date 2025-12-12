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


def print_list(todos: list[storage.Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def cmd_add(path: Path, title: str) -> int:
    todos = storage.load(path)
    next_id = max([t.id for t in todos], default=0) + 1
    todos.append(storage.Todo(id=next_id, title=title, done=False))
    storage.save(path, todos)
    print(f"added [ ] {next_id}: {title}")
    return 0


def cmd_done(path: Path, todo_id: int) -> int:
    todos = storage.load(path)
    for t in todos:
        if t.id == todo_id:
            if t.done:
                print(f"error: already complete: {todo_id}", file=sys.stderr)
                return 1
            t.done = True
            storage.save(path, todos)
            print(f"completed {todo_id}")
            return 0
    print(f"error: no such todo id: {todo_id}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "add":
        return cmd_add(args.file, args.title)
    if args.cmd == "list":
        print_list(storage.load(args.file))
        return 0
    if args.cmd == "done":
        return cmd_done(args.file, args.id)
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
