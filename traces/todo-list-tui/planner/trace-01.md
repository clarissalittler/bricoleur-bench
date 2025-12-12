# Trace 01 (Planner)

The student plans first, then implements each item with a small verification note.

## Plan
- Define data model: list of dicts with `id`, `title`, `done` persisted to `todos.txt`.
- Implement CLI scaffold with subparsers: `add`, `list`, `done`.
- Add persistence helpers `load_todos` and `save_todos` that tolerate missing files.
- Finish commands in order: add -> list -> done.
- Verify flows with sample runs.

## Step 1: Decide storage contract (newline-delimited)

Chooses a dead-simple format that matches the README requirement (“newline-delimited with status flags”):

- One todo per line: `<id>|<status>|<title>`
- `status` is `0` (open) or `1` (done)

Starts with parsing/format helpers so later CLI work is straightforward.

Snapshot: todo.py

```python
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
```

Notes: Keeps it minimal; accepts that a malformed line should error (better than silently corrupting IDs).

## Step 2: Persistence helpers

`todo.py`

```python
from pathlib import Path


def load_todos(path: Path) -> list[Todo]:
    if not path.exists():
        return []
    return [parse_line(line) for line in path.read_text().splitlines(True) if line.strip()]


def save_todos(path: Path, todos: list[Todo]) -> None:
    path.write_text("".join(format_line(t) for t in todos))
```

Notes: Confirms `load_todos` on a missing file returns `[]`.

Snapshot: todo.py
```python
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
```

## Step 3: CLI scaffold

`todo.py`

```python
import argparse
import sys
from pathlib import Path


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
    args = build_parser().parse_args(argv)
    # TODO: dispatch
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Notes: Runs `python todo.py list` and sees an empty exit (dispatch still TODO).

Snapshot: todo.py
```python
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
```

## Step 4: Implement `add`

`todo.py`

```python
if args.cmd == "add":
    todos = load_todos(args.file)
    next_id = (max((t.id for t in todos), default=0) + 1)
    todo = Todo(id=next_id, title=args.title, done=False)
    todos.append(todo)
    save_todos(args.file, todos)
    print(f"added [ ] {todo.id}: {todo.title}")
    return 0
```

Notes: Smoke test:
- `python todo.py add "buy milk"` prints `added [ ] 1: buy milk`
- Confirms `todos.txt` is created.

Snapshot: todo.py
```python
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
    args = build_parser().parse_args(argv)

    if args.cmd == "add":
        todos = load_todos(args.file)
        next_id = max((t.id for t in todos), default=0) + 1
        todo = Todo(id=next_id, title=args.title, done=False)
        todos.append(todo)
        save_todos(args.file, todos)
        print(f"added [ ] {todo.id}: {todo.title}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

## Step 5: Implement `list`

`todo.py`

```python
def print_todos(todos: list[Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


if args.cmd == "list":
    todos = load_todos(args.file)
    print_todos(todos)
    return 0
```

Notes: After two adds, `python todo.py list` prints:
- `[ ] 1: buy milk`
- `[ ] 2: call dentist`

Snapshot: todo.py
```python
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


def print_todos(todos: list[Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "add":
        todos = load_todos(args.file)
        next_id = max((t.id for t in todos), default=0) + 1
        todo = Todo(id=next_id, title=args.title, done=False)
        todos.append(todo)
        save_todos(args.file, todos)
        print(f"added [ ] {todo.id}: {todo.title}")
        return 0

    if args.cmd == "list":
        todos = load_todos(args.file)
        print_todos(todos)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

## Step 6: Implement `done` with validation

`todo.py`

```python
if args.cmd == "done":
    todos = load_todos(args.file)
    for t in todos:
        if t.id == args.id:
            t.done = True
            save_todos(args.file, todos)
            print(f"completed {t.id}")
            return 0
    print(f"error: no such todo id: {args.id}", file=sys.stderr)
    return 1
```

Verification:
- `python todo.py done 1` prints `completed 1`, exit 0
- `python todo.py list` shows `[x] 1: buy milk`
- `python todo.py done 999` prints an error, exit 1

Snapshot: todo.py
```python
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


def print_todos(todos: list[Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "add":
        todos = load_todos(args.file)
        next_id = max((t.id for t in todos), default=0) + 1
        todo = Todo(id=next_id, title=args.title, done=False)
        todos.append(todo)
        save_todos(args.file, todos)
        print(f"added [ ] {todo.id}: {todo.title}")
        return 0

    if args.cmd == "list":
        todos = load_todos(args.file)
        print_todos(todos)
        return 0

    if args.cmd == "done":
        todos = load_todos(args.file)
        for t in todos:
            if t.id == args.id:
                t.done = True
                save_todos(args.file, todos)
                print(f"completed {t.id}")
                return 0
        print(f"error: no such todo id: {args.id}", file=sys.stderr)
        return 1

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```
