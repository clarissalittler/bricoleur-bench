import argparse
import sys
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
    todos = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        todo_id_str, status_str, title = line.split("|", 2)
        todos.append(Todo(int(todo_id_str), title, status_str == "1"))
    return todos


def save(path: Path, todos: list[Todo]) -> None:
    path.write_text("".join(f"{t.id}|{1 if t.done else 0}|{t.title}\n" for t in todos))


def print_list(todos: list[Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def next_id(todos: list[Todo]) -> int:
    return max([t.id for t in todos], default=0) + 1


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=Path, default=Path("todos.txt"))
sub = parser.add_subparsers(dest="cmd", required=True)
add = sub.add_parser("add")
add.add_argument("title")
sub.add_parser("list")
done = sub.add_parser("done")
done.add_argument("id", type=int)
args = parser.parse_args()

todos = load(args.file)

if args.cmd == "add":
    todo = Todo(id=next_id(todos), title=args.title, done=False)
    todos.append(todo)
    save(args.file, todos)
    print(f"added [ ] {todo.id}: {todo.title}")
elif args.cmd == "list":
    print_list(todos)
else:
    print("no such todo", file=sys.stderr)
    raise SystemExit(1)
