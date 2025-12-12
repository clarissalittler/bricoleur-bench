from __future__ import annotations

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
