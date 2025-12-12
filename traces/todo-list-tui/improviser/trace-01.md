# Trace 01 (Improviser)

Alternates between quick hacks and “ok fine, let’s tidy it up”. The student changes direction mid-stream a couple times.

## Step 1: One-file spike (works, ugly output)

Snapshot: todo.py

```python
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
```

Notes: Immediately notices ID is always `0` and `list` is unreadable.

## Step 2: Quick “ID fix” (introduces 0/1 confusion)

Adds an ID counter by using line count, but now “done 1” targets the second line.

```python
lines = FILE.read_text().splitlines() if FILE.exists() else []
todo_id = len(lines)
FILE.write_text("\n".join(lines + [f\"{todo_id}|{title}\"]) + \"\n\")
```

Notes: Runs:
- `python todo.py add "buy milk"`
- `python todo.py add "call dentist"`
Then `python todo.py done 1` (added next) marks the wrong item. Realizes user-facing IDs should probably start at 1.

Snapshot: todo.py
```python
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
```

## Step 3: Switch to a clearer storage line

Migrates to `<id>|<status>|<title>` where status is `0/1`.

```python
def format_line(todo_id: int, done: bool, title: str) -> str:
    return f"{todo_id}|{1 if done else 0}|{title}\n"
```

Notes: Does a manual “file rewrite” once to get old lines into the new format.

Snapshot: todo.py
```python
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
```

## Step 4: Argparse rework (half-migrated for a moment)

Starts converting to subcommands, but leaves the old `sys.argv` block in place and gets double execution once.

```python
import argparse

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)
add = sub.add_parser("add")
add.add_argument("title")
sub.add_parser("list")
done = sub.add_parser("done")
done.add_argument("id", type=int)
args = parser.parse_args()
```

Notes: Deletes the old `sys.argv` branch after noticing two “ok” prints.

Snapshot: todo.py
```python
import argparse
import sys
from pathlib import Path


def format_line(todo_id: int, done: bool, title: str) -> str:
    return f"{todo_id}|{1 if done else 0}|{title}\n"


def load_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text().splitlines(True)


def save_lines(path: Path, lines: list[str]) -> None:
    path.write_text("".join(lines))


def parse_todo_id(raw_line: str) -> int:
    todo_id_str, _rest = raw_line.split("|", 1)
    return int(todo_id_str)


def next_id(lines: list[str]) -> int:
    ids = [parse_todo_id(l.rstrip("\n")) for l in lines if l.strip()]
    return max(ids, default=0) + 1


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=Path, default=Path("todos.txt"))
sub = parser.add_subparsers(dest="cmd", required=True)
add = sub.add_parser("add")
add.add_argument("title")
sub.add_parser("list")
done = sub.add_parser("done")
done.add_argument("id", type=int)
args = parser.parse_args()

lines = load_lines(args.file)

if args.cmd == "add":
    lines.append(format_line(next_id(lines), False, args.title))
    save_lines(args.file, lines)
    print("ok")
elif args.cmd == "list":
    print("".join(lines), end="")
else:
    print("no such todo", file=sys.stderr)
    raise SystemExit(1)
```

## Step 5: Implement add/list with pretty output

`todo.py`

```python
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
```

Notes: Leaves a `print("DEBUG", todos)` in once, sees it on `list`, removes it immediately.

Snapshot: todo.py
```python
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
```

## Step 6: Implement `done` with guardrails

```python
def mark_done(todos: list[Todo], todo_id: int) -> bool:
    for t in todos:
        if t.id == todo_id:
            t.done = True
            return True
    return False
```

Notes:
- If `done` returns false, prints `no such todo` and exits 1.
- Uses `max(id)+1` for new IDs so deletes/reorders won’t reuse IDs.

Final manual run:
- `python todo.py add "buy milk"`
- `python todo.py list` → `[ ] 1: buy milk`
- `python todo.py done 1` → marks complete, persists

Snapshot: todo.py
```python
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


def mark_done(todos: list[Todo], todo_id: int) -> bool:
    for t in todos:
        if t.id == todo_id:
            t.done = True
            return True
    return False


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
elif args.cmd == "done":
    if not mark_done(todos, args.id):
        print("no such todo", file=sys.stderr)
        raise SystemExit(1)
    save(args.file, todos)
    print(f"completed {args.id}")
else:
    raise AssertionError("unreachable")
```
