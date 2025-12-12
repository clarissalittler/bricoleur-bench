from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Todo:
    id: int
    title: str
    done: bool


def load(path: Path) -> list[Todo]:
    if not path.exists():
        return []

    todos: list[Todo] = []
    for raw in path.read_text().splitlines():
        if not raw.strip():
            continue
        todo_id_str, status_str, title = raw.split("|", 2)
        todos.append(Todo(id=int(todo_id_str), done=(status_str == "1"), title=title))
    validate(todos)
    return todos


def save(path: Path, todos: list[Todo]) -> None:
    validate(todos)
    todos_sorted = sorted(todos, key=lambda t: t.id)
    path.write_text("".join(f"{t.id}|{1 if t.done else 0}|{t.title}\n" for t in todos_sorted))


def validate(todos: list[Todo]) -> None:
    ids = [t.id for t in todos]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate todo id")
    if any(t.id < 1 for t in todos):
        raise ValueError("ids must start at 1")
