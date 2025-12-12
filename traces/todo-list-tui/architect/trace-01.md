# Trace 01 (Architect)

### Design notes
- Separate storage from CLI: `storage.py` handles read/write/validation; `todo.py` handles argparse + printing.
- File format stays aligned to the problem README: newline-delimited `id|status|title` (status is `0/1`).
- Error model: validation errors exit 1 with concise message; normal ops exit 0.

## Step 1: Storage contract and invariants

Snapshot: storage.py

```python
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
```

Notes: Makes storage strict: malformed files fail fast instead of “doing something”.

## Step 2: CLI scaffolding (handlers first, then wiring)

`todo.py`

```python
import argparse
import sys
from pathlib import Path

import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a todo")
    add.add_argument("title")

    sub.add_parser("list", help="List todos")

    done = sub.add_parser("done", help="Mark a todo complete")
    done.add_argument("id", type=int)

    return parser
```

Notes: Runs `python todo.py --help` to confirm the CLI contract matches the README.

Snapshot: todo.py
```python
import argparse
import sys
from pathlib import Path

import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a todo")
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

## Step 3: Implement add/list/done (with tiny UX choices)

`todo.py`

```python
def print_list(todos: list[storage.Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def cmd_add(path: Path, title: str) -> int:
    todos = storage.load(path)
    next_id = max([t.id for t in todos], default=0) + 1
    todos.append(storage.Todo(id=next_id, title=title, done=False))
    storage.save(path, todos)
    print(f"added [ ] {next_id}: {title}")
    return 0


def cmd_done(path: Path, todo_id: int) -> int:
    todos = storage.load(path)
    for t in todos:
        if t.id == todo_id:
            if t.done:
                print(f"error: already complete: {todo_id}", file=sys.stderr)
                return 1
            t.done = True
            storage.save(path, todos)
            print(f"completed {todo_id}")
            return 0
    print(f"error: no such todo id: {todo_id}", file=sys.stderr)
    return 1
```

Notes: Leaves “already complete” as an explicit error (small guardrail, not required but consistent).

Snapshot: todo.py
```python
import argparse
import sys
from pathlib import Path

import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a todo")
    add.add_argument("title")

    sub.add_parser("list", help="List todos")

    done = sub.add_parser("done", help="Mark a todo complete")
    done.add_argument("id", type=int)

    return parser


def print_list(todos: list[storage.Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def cmd_add(path: Path, title: str) -> int:
    todos = storage.load(path)
    next_id = max([t.id for t in todos], default=0) + 1
    todos.append(storage.Todo(id=next_id, title=title, done=False))
    storage.save(path, todos)
    print(f"added [ ] {next_id}: {title}")
    return 0


def cmd_done(path: Path, todo_id: int) -> int:
    todos = storage.load(path)
    for t in todos:
        if t.id == todo_id:
            if t.done:
                print(f"error: already complete: {todo_id}", file=sys.stderr)
                return 1
            t.done = True
            storage.save(path, todos)
            print(f"completed {todo_id}")
            return 0
    print(f"error: no such todo id: {todo_id}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "add":
        return cmd_add(args.file, args.title)
    if args.cmd == "list":
        print_list(storage.load(args.file))
        return 0
    if args.cmd == "done":
        return cmd_done(args.file, args.id)
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

## Step 4: Wire `main` and capture storage errors cleanly

`todo.py`

```python
def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "add":
            return cmd_add(args.file, args.title)
        if args.cmd == "list":
            print_list(storage.load(args.file))
            return 0
        if args.cmd == "done":
            return cmd_done(args.file, args.id)
        raise AssertionError("unreachable")
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
```

Notes: This makes “corrupt file” failures present as a clean one-line error.

Snapshot: todo.py
```python
import argparse
import sys
from pathlib import Path

import storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    parser.add_argument("--file", type=Path, default=Path("todos.txt"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a todo")
    add.add_argument("title")

    sub.add_parser("list", help="List todos")

    done = sub.add_parser("done", help="Mark a todo complete")
    done.add_argument("id", type=int)

    return parser


def print_list(todos: list[storage.Todo]) -> None:
    for t in todos:
        mark = "x" if t.done else " "
        print(f"[{mark}] {t.id}: {t.title}")


def cmd_add(path: Path, title: str) -> int:
    todos = storage.load(path)
    next_id = max([t.id for t in todos], default=0) + 1
    todos.append(storage.Todo(id=next_id, title=title, done=False))
    storage.save(path, todos)
    print(f"added [ ] {next_id}: {title}")
    return 0


def cmd_done(path: Path, todo_id: int) -> int:
    todos = storage.load(path)
    for t in todos:
        if t.id == todo_id:
            if t.done:
                print(f"error: already complete: {todo_id}", file=sys.stderr)
                return 1
            t.done = True
            storage.save(path, todos)
            print(f"completed {todo_id}")
            return 0
    print(f"error: no such todo id: {todo_id}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "add":
            return cmd_add(args.file, args.title)
        if args.cmd == "list":
            print_list(storage.load(args.file))
            return 0
        if args.cmd == "done":
            return cmd_done(args.file, args.id)
        raise AssertionError("unreachable")
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

## Step 5: Dry run

- `python todo.py add "buy milk"` → `added [ ] 1: buy milk`
- `python todo.py list` → `[ ] 1: buy milk`
- `python todo.py done 1` → `completed 1`
- `python todo.py list` → `[x] 1: buy milk`
