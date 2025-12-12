import sys
from pathlib import Path

FILE = Path("todos.txt")

cmd = sys.argv[1]

if cmd == "add":
    title = sys.argv[2]
    FILE.write_text(FILE.read_text() + f"0|{title}\n" if FILE.exists() else f"0|{title}\n")
    print("ok")
elif cmd == "list":
    if FILE.exists():
        print(FILE.read_text(), end="")
