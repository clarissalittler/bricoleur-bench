from __future__ import annotations

from dataclasses import dataclass


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
