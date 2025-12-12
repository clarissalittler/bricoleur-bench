import sys
from pathlib import Path

FILE = Path("todos.txt")


def format_line(todo_id: int, done: bool, title: str) -> str:
    return f"{todo_id}|{1 if done else 0}|{title}\n"


def parse_ids(lines: list[str]) -> list[int]:
    ids: list[int] = []
    for raw in lines:
        if not raw.strip():
            continue
        todo_id_str, _rest = raw.split("|", 1)
        ids.append(int(todo_id_str))
    return ids


cmd = sys.argv[1]

if cmd == "add":
    title = sys.argv[2]
    lines = FILE.read_text().splitlines(True) if FILE.exists() else []
    next_id = max(parse_ids([l.rstrip("\n") for l in lines]), default=0) + 1
    lines.append(format_line(next_id, False, title))
    FILE.write_text("".join(lines))
    print("ok")
elif cmd == "list":
    if FILE.exists():
        print(FILE.read_text(), end="")
