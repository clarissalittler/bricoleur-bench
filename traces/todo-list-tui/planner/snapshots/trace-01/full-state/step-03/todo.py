from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False


def parse_line(line: str) -> Todo:
    raw = line.rstrip("\n")
    todo_id_str, status_str, title = raw.split("|", 2)
    return Todo(id=int(todo_id_str), done=(status_str == "1"), title=title)


def format_line(todo: Todo) -> str:
    status = "1" if todo.done else "0"
    return f"{todo.id}|{status}|{todo.title}\n"


def load_todos(path: Path) -> list[Todo]:
    if not path.exists():
        return []
    return [parse_line(line) for line in path.read_text().splitlines(True) if line.strip()]


def save_todos(path: Path, todos: list[Todo]) -> None:
    path.write_text("".join(format_line(t) for t in todos))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo.py", description="A tiny todo CLI")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a new todo")
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
