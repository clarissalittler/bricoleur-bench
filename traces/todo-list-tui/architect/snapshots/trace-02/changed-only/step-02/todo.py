import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False


def parse_line(line: str) -> Todo | None:
    raw = line.rstrip("\n")
    parts = raw.split("|", 2)
    if len(parts) != 3:
        return None
    todo_id_str, status_str, title = parts
    try:
        todo_id = int(todo_id_str)
    except ValueError:
        return None
    if status_str not in ("0", "1"):
        return None
    return Todo(id=todo_id, done=(status_str == "1"), title=title)


def load_todos(path: Path) -> list[Todo]:
    if not path.exists():
        return []
    todos: list[Todo] = []
    for line in path.read_text().splitlines(True):
        if not line.strip():
            continue
        todo = parse_line(line)
        if todo is None:
            continue
        todos.append(todo)
    return todos


def save_todos(path: Path, todos: list[Todo]) -> None:
    todos_sorted = sorted(todos, key=lambda t: t.id)
    path.write_text("".join(f"{t.id}|{1 if t.done else 0}|{t.title}\n" for t in todos_sorted))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo.py")
    p.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = p.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("title")
    sub.add_parser("list")
    done = sub.add_parser("done")
    done.add_argument("id", type=int)
    rm = sub.add_parser("rm")
    rm.add_argument("id", type=int)
    return p


def print_list(todos: list[Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    todos = load_todos(args.file)

    if args.cmd == "add":
        next_id = max((t.id for t in todos), default=0) + 1
        todos.append(Todo(id=next_id, title=args.title, done=False))
        save_todos(args.file, todos)
        print(f"added [ ] {next_id}: {args.title}")
        return 0

    if args.cmd == "list":
        print_list(todos)
        return 0

    if args.cmd == "done":
        for t in todos:
            if t.id == args.id:
                t.done = True
                save_todos(args.file, todos)
                print(f"completed {t.id}")
                return 0
        print(f"error: no such todo id: {args.id}", file=sys.stderr)
        return 1

    if args.cmd == "rm":
        kept = [t for t in todos if t.id != args.id]
        if len(kept) == len(todos):
            print(f"error: no such todo id: {args.id}", file=sys.stderr)
            return 1
        save_todos(args.file, kept)
        print(f"removed {args.id}")
        return 0

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
