import sys
from pathlib import Path

FILE = Path("todos.txt")

cmd = sys.argv[1]

if cmd == "add":
    title = sys.argv[2]
    lines = FILE.read_text().splitlines() if FILE.exists() else []
    todo_id = len(lines)  # starts at 0
    lines.append(f"{todo_id}|{title}")
    FILE.write_text("\n".join(lines) + "\n")
    print("ok")
elif cmd == "list":
    if FILE.exists():
        print(FILE.read_text(), end="")
