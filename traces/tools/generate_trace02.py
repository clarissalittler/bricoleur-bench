#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


PERSONAS = ["bricoleur", "improviser", "planner", "debugger", "optimizer", "skeptic", "architect"]


@dataclass(frozen=True)
class ProblemSpec:
    slug: str
    title: str


PROBLEMS = [
    ProblemSpec(slug="temperature-converter", title="Temperature Converter CLI"),
    ProblemSpec(slug="word-frequency-counter", title="Word Frequency Counter"),
    ProblemSpec(slug="todo-list-tui", title="Todo List TUI"),
    ProblemSpec(slug="ascii-art-poster", title="ASCII Art Poster"),
    ProblemSpec(slug="interactive-fiction-engine", title="Interactive Fiction Engine"),
    ProblemSpec(slug="conway-life-sim", title="Conway’s Game of Life"),
    ProblemSpec(slug="haiku-generator", title="Haiku / Microfiction Generator"),
    ProblemSpec(slug="maze-generator-solver", title="Maze Generator + Solver"),
    ProblemSpec(slug="svg-logo-generator", title="SVG Logo Generator"),
]


def write(path: Path, text: str, *, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return
    path.write_text(text, encoding="utf-8")


def header(persona: str, problem: str) -> str:
    return f"# Trace 02 – {persona.title()} ({problem})\n\n"


def temp_converter(persona: str) -> str:
    # Trace-02: focus on polish + exit codes + strict parsing.
    s1 = """## Step 1: Baseline works; tighten UX

Snapshot: convert.py
```python
import argparse
import math
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Convert temperatures.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
    group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
    parser.add_argument("value", type=float, help="Temperature to convert")
    args = parser.parse_args()

    if not math.isfinite(args.value):
        print("error: temperature must be finite", file=sys.stderr)
        return 1

    if args.to_f:
        result = args.value * 9 / 5 + 32
        unit = "F"
    else:
        result = (args.value - 32) * 5 / 9
        unit = "C"

    print(f"{result:.2f}{unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Better help + clearer errors

Snapshot: convert.py
```python
import argparse
import math
import sys


def finite_float(raw: str) -> float:
    try:
        value = float(raw)
    except ValueError as e:
        raise argparse.ArgumentTypeError("value must be a number") from e
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError("value must be finite")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Convert temperatures.\n\nExamples:\n  python convert.py --to-f 0\n  python convert.py --to-c 212",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
    group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
    parser.add_argument("value", type=finite_float, help="Temperature to convert")
    args = parser.parse_args()

    if args.to_f:
        result = args.value * 9 / 5 + 32
        unit = "F"
    else:
        result = (args.value - 32) * 5 / 9
        unit = "C"

    print(f"{result:.2f}{unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def word_counter(persona: str) -> str:
    # Trace-02: determinism + tie-breaking + unicode-ish handling.
    s1 = """## Step 1: Deterministic ordering for ties

Snapshot: count_words.py
```python
import argparse
import re
import sys
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z']+")


def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    tokens = [t.strip(\"'\") for t in raw]
    return [t for t in tokens if t]


def main() -> int:
    p = argparse.ArgumentParser(prog="count_words.py")
    p.add_argument("path", type=Path)
    p.add_argument("--top", type=int, default=None)
    args = p.parse_args()

    try:
        text = args.path.read_text(encoding=\"utf-8\")
    except FileNotFoundError:
        print(f\"missing file: {args.path}\", file=sys.stderr)
        return 1

    tokens = tokenize(text)
    if not tokens:
        return 0

    counts = Counter(tokens)
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        items = items[: args.top]
    for word, count in items:
        print(f\"{word}: {count}\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Slightly broader tokenization (keeps default stable)

Snapshot: count_words.py
```python
import argparse
import re
import sys
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r\"[A-Za-z']+\")


def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    tokens = [t.strip(\"'\") for t in raw]
    return [t for t in tokens if t]


def positive_int(raw: str) -> int:
    try:
        n = int(raw)
    except ValueError as e:
        raise argparse.ArgumentTypeError(\"--top must be an integer\") from e
    if n < 1:
        raise argparse.ArgumentTypeError(\"--top must be positive\")
    return n


def main() -> int:
    p = argparse.ArgumentParser(
        prog=\"count_words.py\",
        description=\"Count word frequencies.\\n\\nExample:\\n  python count_words.py sample.txt --top 5\",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(\"path\", type=Path)
    p.add_argument(\"--top\", type=positive_int, default=None)
    args = p.parse_args()

    try:
        text = args.path.read_text(encoding=\"utf-8\")
    except FileNotFoundError:
        print(f\"missing file: {args.path}\", file=sys.stderr)
        return 1

    tokens = tokenize(text)
    if not tokens:
        return 0

    counts = Counter(tokens)
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        items = items[: args.top]
    for word, count in items:
        print(f\"{word}: {count}\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def todo_tui(persona: str) -> str:
    # Trace-02: malformed storage handling + new 'rm' command (creative but testable).
    s1 = """## Step 1: Add strict parsing and skip malformed lines

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
    done: bool = False


def parse_line(line: str) -> Todo | None:
    raw = line.rstrip(\"\\n\")
    parts = raw.split(\"|\", 2)
    if len(parts) != 3:
        return None
    todo_id_str, status_str, title = parts
    try:
        todo_id = int(todo_id_str)
    except ValueError:
        return None
    if status_str not in (\"0\", \"1\"):
        return None
    return Todo(id=todo_id, done=(status_str == \"1\"), title=title)


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
    path.write_text(\"\".join(f\"{t.id}|{1 if t.done else 0}|{t.title}\\n\" for t in todos_sorted))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=\"todo.py\")
    p.add_argument(\"--file\", type=Path, default=Path(\"todos.txt\"))
    sub = p.add_subparsers(dest=\"cmd\", required=True)
    add = sub.add_parser(\"add\")
    add.add_argument(\"title\")
    sub.add_parser(\"list\")
    done = sub.add_parser(\"done\")
    done.add_argument(\"id\", type=int)
    return p


def print_list(todos: list[Todo]) -> None:
    for t in todos:
        mark = \"x\" if t.done else \" \"
        print(f\"[{mark}] {t.id}: {t.title}\")


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    todos = load_todos(args.file)

    if args.cmd == \"add\":
        next_id = max((t.id for t in todos), default=0) + 1
        todos.append(Todo(id=next_id, title=args.title, done=False))
        save_todos(args.file, todos)
        print(f\"added [ ] {next_id}: {args.title}\")
        return 0

    if args.cmd == \"list\":
        print_list(todos)
        return 0

    if args.cmd == \"done\":
        for t in todos:
            if t.id == args.id:
                t.done = True
                save_todos(args.file, todos)
                print(f\"completed {t.id}\")
                return 0
        print(f\"error: no such todo id: {args.id}\", file=sys.stderr)
        return 1

    raise AssertionError(\"unreachable\")


if __name__ == \"__main__\":
    raise SystemExit(main(sys.argv[1:]))
```
"""
    s2 = """## Step 2: Add `rm <id>` command

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
    done: bool = False


def parse_line(line: str) -> Todo | None:
    raw = line.rstrip(\"\\n\")
    parts = raw.split(\"|\", 2)
    if len(parts) != 3:
        return None
    todo_id_str, status_str, title = parts
    try:
        todo_id = int(todo_id_str)
    except ValueError:
        return None
    if status_str not in (\"0\", \"1\"):
        return None
    return Todo(id=todo_id, done=(status_str == \"1\"), title=title)


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
    path.write_text(\"\".join(f\"{t.id}|{1 if t.done else 0}|{t.title}\\n\" for t in todos_sorted))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=\"todo.py\")
    p.add_argument(\"--file\", type=Path, default=Path(\"todos.txt\"))
    sub = p.add_subparsers(dest=\"cmd\", required=True)
    add = sub.add_parser(\"add\")
    add.add_argument(\"title\")
    sub.add_parser(\"list\")
    done = sub.add_parser(\"done\")
    done.add_argument(\"id\", type=int)
    rm = sub.add_parser(\"rm\")
    rm.add_argument(\"id\", type=int)
    return p


def print_list(todos: list[Todo]) -> None:
    for t in todos:
        mark = \"x\" if t.done else \" \"
        print(f\"[{mark}] {t.id}: {t.title}\")


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    todos = load_todos(args.file)

    if args.cmd == \"add\":
        next_id = max((t.id for t in todos), default=0) + 1
        todos.append(Todo(id=next_id, title=args.title, done=False))
        save_todos(args.file, todos)
        print(f\"added [ ] {next_id}: {args.title}\")
        return 0

    if args.cmd == \"list\":
        print_list(todos)
        return 0

    if args.cmd == \"done\":
        for t in todos:
            if t.id == args.id:
                t.done = True
                save_todos(args.file, todos)
                print(f\"completed {t.id}\")
                return 0
        print(f\"error: no such todo id: {args.id}\", file=sys.stderr)
        return 1

    if args.cmd == \"rm\":
        kept = [t for t in todos if t.id != args.id]
        if len(kept) == len(todos):
            print(f\"error: no such todo id: {args.id}\", file=sys.stderr)
            return 1
        save_todos(args.file, kept)
        print(f\"removed {args.id}\")
        return 0

    raise AssertionError(\"unreachable\")


if __name__ == \"__main__\":
    raise SystemExit(main(sys.argv[1:]))
```
"""
    return s1 + "\n" + s2


def ascii_poster(persona: str) -> str:
    # Trace-02: creative style flag `--theme` while keeping default stable.
    s1 = """## Step 1: Add theme without changing default

Snapshot: poster.py
```python
import argparse
import textwrap


THEMES = {
    \"default\": {\"corner\": \"+\", \"h\": \"-\", \"v\": \"|\"},
    \"bubble\": {\"corner\": \"o\", \"h\": \"-\", \"v\": \"|\"},
}


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [\"\"]


def align_line(line: str, width: int, align: str) -> str:
    if align == \"left\":
        return line.ljust(width)
    if align == \"right\":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str, theme: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == \"none\":
        return \"\\n\".join(lines) + \"\\n\"

    t = THEMES[theme]
    top = t[\"corner\"] + t[\"h\"] * (width + 2) + t[\"corner\"] + \"\\n\"
    body = \"\".join(t[\"v\"] + \" \" + line + \" \" + t[\"v\"] + \"\\n\" for line in lines)
    bot = top
    return top + body + bot


def main() -> int:
    p = argparse.ArgumentParser(prog=\"poster.py\")
    p.add_argument(\"message\")
    p.add_argument(\"--width\", type=int, default=20)
    p.add_argument(\"--align\", choices=[\"left\", \"center\", \"right\"], default=\"left\")
    p.add_argument(\"--border\", choices=[\"ascii\", \"none\"], default=\"ascii\")
    p.add_argument(\"--theme\", choices=sorted(THEMES.keys()), default=\"default\")
    args = p.parse_args()

    if args.width < 1:
        raise SystemExit(\"error: --width must be >= 1\")
    print(render(args.message, args.width, args.align, args.border, args.theme), end=\"\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Make default theme explicit for tests

Snapshot: poster.py
```python
import argparse
import textwrap


THEMES = {
    \"default\": {\"corner\": \"+\", \"h\": \"-\", \"v\": \"|\"},
    \"bubble\": {\"corner\": \"o\", \"h\": \"-\", \"v\": \"|\"},
}


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [\"\"]


def align_line(line: str, width: int, align: str) -> str:
    if align == \"left\":
        return line.ljust(width)
    if align == \"right\":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str, theme: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == \"none\":
        return \"\\n\".join(lines) + \"\\n\"

    t = THEMES[theme]
    top = t[\"corner\"] + t[\"h\"] * (width + 2) + t[\"corner\"] + \"\\n\"
    body = \"\".join(t[\"v\"] + \" \" + line + \" \" + t[\"v\"] + \"\\n\" for line in lines)
    return top + body + top


def main() -> int:
    p = argparse.ArgumentParser(
        prog=\"poster.py\",
        description=\"ASCII poster. Default theme is deterministic.\",
    )
    p.add_argument(\"message\")
    p.add_argument(\"--width\", type=int, default=20)
    p.add_argument(\"--align\", choices=[\"left\", \"center\", \"right\"], default=\"left\")
    p.add_argument(\"--border\", choices=[\"ascii\", \"none\"], default=\"ascii\")
    p.add_argument(\"--theme\", choices=sorted(THEMES.keys()), default=\"default\")
    args = p.parse_args()

    if args.width < 1:
        raise SystemExit(\"error: --width must be >= 1\")
    print(render(args.message, args.width, args.align, args.border, args.theme), end=\"\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def fiction_engine(persona: str) -> str:
    # Trace-02: handle invalid story references + add --strict.
    s1 = """## Step 1: Add strict validation of story graph

Snapshot: play.py
```python
import argparse
import json
import sys


def load_story(path: str) -> dict:
    with open(path, \"r\", encoding=\"utf-8\") as f:
        return json.load(f)


def validate(story: dict) -> list[str]:
    errors: list[str] = []
    if \"start\" not in story or \"nodes\" not in story:
        return [\"missing start/nodes\"]
    nodes = story[\"nodes\"]
    start = story[\"start\"]
    if start not in nodes:
        errors.append(f\"start node not found: {start}\")
    for node_id, node in nodes.items():
        for ch in node.get(\"choices\", []):
            to = ch.get(\"to\")
            if to not in nodes:
                errors.append(f\"{node_id}: choice target missing: {to}\")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(prog=\"play.py\")
    p.add_argument(\"story\")
    p.add_argument(\"--strict\", action=\"store_true\")
    args = p.parse_args()

    story = load_story(args.story)
    errs = validate(story)
    if errs and args.strict:
        for e in errs:
            print(f\"error: {e}\", file=sys.stderr)
        return 1

    nodes = story[\"nodes\"]
    cur = story[\"start\"]
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get(\"sets\", []))
        print(node.get(\"text\", \"\"))
        choices = []
        for c in node.get(\"choices\", []):
            req = c.get(\"requires\", [])
            if all(r in flags for r in req):
                choices.append(c)
        if node.get(\"end\") or not choices:
            return 0
        for i, c in enumerate(choices, start=1):
            print(f\"{i}. {c['label']}\")
        raw = input(\"> \").strip()
        try:
            idx = int(raw)
        except ValueError:
            print(\"Please enter a number.\\n\")
            continue
        if idx < 1 or idx > len(choices):
            print(\"Invalid choice.\\n\")
            continue
        cur = choices[idx - 1][\"to\"]
        print()


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Provide a small second example story with a deliberate bug

Snapshot: example-story-02.json
```json
{
  \"start\": \"start\",
  \"nodes\": {
    \"start\": {
      \"text\": \"A fork in the road.\",
      \"choices\": [
        { \"label\": \"Go left\", \"to\": \"left\" },
        { \"label\": \"Go right\", \"to\": \"missing_node\" }
      ]
    },
    \"left\": { \"text\": \"Left is quiet.\", \"end\": true, \"choices\": [] }
  }
}
```

Snapshot: play.py
```python
import argparse
import json
import sys


def load_story(path: str) -> dict:
    with open(path, \"r\", encoding=\"utf-8\") as f:
        return json.load(f)


def validate(story: dict) -> list[str]:
    errors: list[str] = []
    if \"start\" not in story or \"nodes\" not in story:
        return [\"missing start/nodes\"]
    nodes = story[\"nodes\"]
    start = story[\"start\"]
    if start not in nodes:
        errors.append(f\"start node not found: {start}\")
    for node_id, node in nodes.items():
        for ch in node.get(\"choices\", []):
            to = ch.get(\"to\")
            if to not in nodes:
                errors.append(f\"{node_id}: choice target missing: {to}\")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(prog=\"play.py\")
    p.add_argument(\"story\")
    p.add_argument(\"--strict\", action=\"store_true\")
    args = p.parse_args()

    story = load_story(args.story)
    errs = validate(story)
    if errs and args.strict:
        for e in errs:
            print(f\"error: {e}\", file=sys.stderr)
        return 1

    nodes = story[\"nodes\"]
    cur = story[\"start\"]
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get(\"sets\", []))
        print(node.get(\"text\", \"\"))
        choices = []
        for c in node.get(\"choices\", []):
            req = c.get(\"requires\", [])
            if all(r in flags for r in req):
                choices.append(c)
        if node.get(\"end\") or not choices:
            return 0
        for i, c in enumerate(choices, start=1):
            print(f\"{i}. {c['label']}\")
        raw = input(\"> \").strip()
        try:
            idx = int(raw)
        except ValueError:
            print(\"Please enter a number.\\n\")
            continue
        if idx < 1 or idx > len(choices):
            print(\"Invalid choice.\\n\")
            continue
        cur = choices[idx - 1][\"to\"]
        if cur not in nodes:
            print(f\"error: story references missing node: {cur}\", file=sys.stderr)
            return 1
        print()


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def conway_life(persona: str) -> str:
    # Trace-02: add --wrap mode (creative-ish) while keeping default stable.
    s1 = """## Step 1: Add `--wrap` option

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip(\"\\n\") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit(\"error: empty pattern\")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit(\"error: ragged grid\")
    for l in raw:
        for ch in l:
            if ch not in (\".\", \"#\"):\n                raise SystemExit(\"error: grid must contain only . and #\")\n
    return raw


def step(lines: list[str], wrap: bool) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if wrap:
                    ny %= h
                    nx %= w
                    if lines[ny][nx] == \"#\":
                        n += 1
                else:
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == \"#\":
                        n += 1
            alive = lines[y][x] == \"#\"
            row.append(\"#\" if (alive and n in (2, 3)) or ((not alive) and n == 3) else \".\")
        out.append(\"\".join(row))
    return out


def main() -> int:
    p = argparse.ArgumentParser(prog=\"life.py\")
    p.add_argument(\"--steps\", type=int, required=True)
    p.add_argument(\"--wrap\", action=\"store_true\")
    p.add_argument(\"pattern\")
    args = p.parse_args()
    if args.steps < 0:
        print(\"error: --steps must be >= 0\", file=sys.stderr)
        return 1
    lines = parse_lines(args.pattern)
    print(\"\\n\".join(lines))
    for _ in range(args.steps):
        print()
        lines = step(lines, wrap=args.wrap)
        print(\"\\n\".join(lines))
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Keep default rendering stable; add `--alive` and `--dead` chars

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip(\"\\n\") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit(\"error: empty pattern\")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit(\"error: ragged grid\")
    for l in raw:
        for ch in l:
            if ch not in (\".\", \"#\"):\n                raise SystemExit(\"error: grid must contain only . and #\")\n
    return raw


def step(lines: list[str], wrap: bool) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if wrap:
                    ny %= h
                    nx %= w
                    if lines[ny][nx] == \"#\":
                        n += 1
                else:
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == \"#\":
                        n += 1
            alive = lines[y][x] == \"#\"
            row.append(\"#\" if (alive and n in (2, 3)) or ((not alive) and n == 3) else \".\")
        out.append(\"\".join(row))
    return out


def render(lines: list[str], alive: str, dead: str) -> str:
    if alive == \"#\" and dead == \".\":
        return \"\\n\".join(lines)
    return \"\\n\".join(\"\".join(alive if ch == \"#\" else dead for ch in row) for row in lines)


def main() -> int:
    p = argparse.ArgumentParser(prog=\"life.py\")
    p.add_argument(\"--steps\", type=int, required=True)
    p.add_argument(\"--wrap\", action=\"store_true\")
    p.add_argument(\"--alive\", default=\"#\")
    p.add_argument(\"--dead\", default=\".\")
    p.add_argument(\"pattern\")
    args = p.parse_args()
    if args.steps < 0:
        print(\"error: --steps must be >= 0\", file=sys.stderr)
        return 1
    lines = parse_lines(args.pattern)
    print(render(lines, args.alive, args.dead))
    for _ in range(args.steps):
        print()
        lines = step(lines, wrap=args.wrap)
        print(render(lines, args.alive, args.dead))
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def haiku(persona: str) -> str:
    # Trace-02: add --theme (bias words) while keeping determinism.
    s1 = """## Step 1: Add optional theme word bias

Snapshot: haiku.py
```python
import argparse
import random
import sys


def read_words(path: str) -> list[str]:
    try:
        raw = [w.strip() for w in open(path).read().splitlines()]
    except FileNotFoundError:
        print(f\"error: missing word list: {path}\", file=sys.stderr)
        raise SystemExit(1)
    words = [w for w in raw if w]
    if not words:
        print(\"error: word list is empty\", file=sys.stderr)
        raise SystemExit(1)
    return words


def biased_choice(rng: random.Random, words: list[str], theme: str | None) -> str:
    if not theme:
        return rng.choice(words)
    themed = [w for w in words if theme.lower() in w.lower()]
    pool = themed if themed else words
    return rng.choice(pool)


def gen_haiku(rng: random.Random, words: list[str], theme: str | None) -> str:
    return \"\\n\".join(\" \".join(biased_choice(rng, words, theme) for _ in range(3)) for _ in range(3)) + \"\\n\"


def gen_micro(rng: random.Random, words: list[str], theme: str | None) -> str:
    a = \" \".join(biased_choice(rng, words, theme) for _ in range(8)).capitalize() + \".\"
    return a + \"\\n\"


def main() -> int:
    p = argparse.ArgumentParser(prog=\"haiku.py\")
    p.add_argument(\"--seed\", type=int, required=True)
    p.add_argument(\"--style\", choices=[\"haiku\", \"micro\"], default=\"haiku\")
    p.add_argument(\"--theme\", default=None)
    p.add_argument(\"words\")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    out = gen_micro(rng, words, args.theme) if args.style == \"micro\" else gen_haiku(rng, words, args.theme)
    print(out, end=\"\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Make output shape stricter for micro style

Snapshot: haiku.py
```python
import argparse
import random
import sys


def read_words(path: str) -> list[str]:
    try:
        raw = [w.strip() for w in open(path).read().splitlines()]
    except FileNotFoundError:
        print(f\"error: missing word list: {path}\", file=sys.stderr)
        raise SystemExit(1)
    words = [w for w in raw if w]
    if not words:
        print(\"error: word list is empty\", file=sys.stderr)
        raise SystemExit(1)
    return words


def biased_choice(rng: random.Random, words: list[str], theme: str | None) -> str:
    if not theme:
        return rng.choice(words)
    themed = [w for w in words if theme.lower() in w.lower()]
    pool = themed if themed else words
    return rng.choice(pool)


def gen_haiku(rng: random.Random, words: list[str], theme: str | None) -> str:
    return \"\\n\".join(\" \".join(biased_choice(rng, words, theme) for _ in range(3)) for _ in range(3)) + \"\\n\"


def gen_micro(rng: random.Random, words: list[str], theme: str | None) -> str:
    sentence = \" \".join(biased_choice(rng, words, theme) for _ in range(10)).capitalize() + \".\"
    return sentence + \"\\n\"


def main() -> int:
    p = argparse.ArgumentParser(prog=\"haiku.py\")
    p.add_argument(\"--seed\", type=int, required=True)
    p.add_argument(\"--style\", choices=[\"haiku\", \"micro\"], default=\"haiku\")
    p.add_argument(\"--theme\", default=None)
    p.add_argument(\"words\")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    if args.style == \"micro\":
        print(gen_micro(rng, words, args.theme), end=\"\")
        return 0
    print(gen_haiku(rng, words, args.theme), end=\"\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def maze(persona: str) -> str:
    # Trace-02: add optional path overlay output for solver (--show-path).
    s1 = """## Step 1: Keep solver output stable; add optional `--show-path`

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


ALLOWED = {\"#\", \".\", \"S\", \"E\"}


def parse(path: str):
    lines = [l.rstrip(\"\\n\") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise SystemExit(\"error: empty maze\")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise SystemExit(\"error: ragged maze\")
    grid = [list(l) for l in lines]
    for row in grid:
        for ch in row:
            if ch not in ALLOWED:
                raise SystemExit(\"error: unknown character in maze\")
    return grid


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def solve_path(grid):
    start = find(grid, \"S\")
    end = find(grid, \"E\")
    if not start or not end:
        raise SystemExit(\"error: missing S or E\")
    w = len(grid[0])
    h = len(grid)
    q = deque([start])
    prev = {start: None}
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in prev:
                if grid[ny][nx] in (\".\", \"E\"):\n                    prev[(nx, ny)] = (x, y)\n                    q.append((nx, ny))\n
    if end not in prev:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def gen(width: int, height: int, seed: int):
    rng = random.Random(seed)
    grid = [[\"#\"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = \".\"
    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    x, y = sx, sy
    path = {(x, y)}
    while (x, y) != (ex, ey):
        if rng.random() < 0.5 and x < ex:
            x += 1
        elif y < ey:
            y += 1
        path.add((x, y))
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.30:
                grid[y][x] = \"#\"
    grid[sy][sx] = \"S\"
    grid[ey][ex] = \"E\"
    return grid


def print_grid(grid):
    for row in grid:
        print(\"\".join(row))


def overlay(grid, path):
    g = [row[:] for row in grid]
    for (x, y) in path:
        if g[y][x] == \".\":
            g[y][x] = \"*\"
    return g


def main() -> int:
    p = argparse.ArgumentParser(prog=\"maze.py\")
    sub = p.add_subparsers(dest=\"cmd\", required=True)
    g = sub.add_parser(\"gen\")
    g.add_argument(\"--width\", type=int, required=True)
    g.add_argument(\"--height\", type=int, required=True)
    g.add_argument(\"--seed\", type=int, required=True)
    s = sub.add_parser(\"solve\")
    s.add_argument(\"--show-path\", action=\"store_true\")
    s.add_argument(\"maze\")
    args = p.parse_args()

    if args.cmd == \"gen\":
        print_grid(gen(args.width, args.height, args.seed))
        return 0

    grid = parse(args.maze)
    path = solve_path(grid)
    if path is None:
        print(\"error: unsolvable\", file=sys.stderr)
        return 1
    print(f\"path_length={len(path)-1}\")
    if args.show_path:
        print()
        print_grid(overlay(grid, path))
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Keep parser strict about exactly one S/E

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


ALLOWED = {\"#\", \".\", \"S\", \"E\"}


def parse(path: str):
    lines = [l.rstrip(\"\\n\") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise SystemExit(\"error: empty maze\")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise SystemExit(\"error: ragged maze\")
    grid = [list(l) for l in lines]
    for row in grid:
        for ch in row:
            if ch not in ALLOWED:
                raise SystemExit(\"error: unknown character in maze\")
    if sum(ch == \"S\" for row in grid for ch in row) != 1:
        raise SystemExit(\"error: maze must contain exactly one S\")
    if sum(ch == \"E\" for row in grid for ch in row) != 1:
        raise SystemExit(\"error: maze must contain exactly one E\")
    return grid


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    raise AssertionError(\"unreachable\")


def solve_path(grid):
    start = find(grid, \"S\")
    end = find(grid, \"E\")
    w = len(grid[0])
    h = len(grid)
    q = deque([start])
    prev = {start: None}
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in prev:
                if grid[ny][nx] in (\".\", \"E\"):\n                    prev[(nx, ny)] = (x, y)\n                    q.append((nx, ny))\n
    if end not in prev:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def gen(width: int, height: int, seed: int):
    if width < 3 or height < 3:
        raise SystemExit(\"error: width/height must be >= 3\")
    rng = random.Random(seed)
    grid = [[\"#\"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = \".\"
    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    x, y = sx, sy
    path = {(x, y)}
    while (x, y) != (ex, ey):
        if rng.random() < 0.5 and x < ex:
            x += 1
        elif y < ey:
            y += 1
        path.add((x, y))
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.30:
                grid[y][x] = \"#\"
    grid[sy][sx] = \"S\"
    grid[ey][ex] = \"E\"
    return grid


def print_grid(grid):
    for row in grid:
        print(\"\".join(row))


def overlay(grid, path):
    g = [row[:] for row in grid]
    for (x, y) in path:
        if g[y][x] == \".\":
            g[y][x] = \"*\"
    return g


def main() -> int:
    p = argparse.ArgumentParser(prog=\"maze.py\")
    sub = p.add_subparsers(dest=\"cmd\", required=True)
    g = sub.add_parser(\"gen\")
    g.add_argument(\"--width\", type=int, required=True)
    g.add_argument(\"--height\", type=int, required=True)
    g.add_argument(\"--seed\", type=int, required=True)
    s = sub.add_parser(\"solve\")
    s.add_argument(\"--show-path\", action=\"store_true\")
    s.add_argument(\"maze\")
    args = p.parse_args()

    if args.cmd == \"gen\":
        print_grid(gen(args.width, args.height, args.seed))
        return 0

    grid = parse(args.maze)
    path = solve_path(grid)
    if path is None:
        print(\"error: unsolvable\", file=sys.stderr)
        return 1
    print(f\"path_length={len(path)-1}\")
    if args.show_path:
        print()
        print_grid(overlay(grid, path))
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def svg_logo(persona: str) -> str:
    # Trace-02: add basic text fitting and keep determinism.
    s1 = """## Step 1: Add font-size fitting loop

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    \"default\": {\"bg\": \"#111111\", \"fg\": \"#ffffff\"},
    \"invert\": {\"bg\": \"#ffffff\", \"fg\": \"#111111\"},
}


def fit_font_size(text: str, width: int, base: int = 32) -> int:
    # crude heuristic: assume average char width ~ 0.6em
    if not text:
        return base
    max_chars = max(1, int((width - 40) / (base * 0.6)))
    if len(text) <= max_chars:
        return base
    scale = max_chars / len(text)
    return max(10, int(base * scale))


def main() -> int:
    p = argparse.ArgumentParser(prog=\"logo.py\")
    p.add_argument(\"text\")
    p.add_argument(\"--width\", type=int, default=300)
    p.add_argument(\"--height\", type=int, default=120)
    p.add_argument(\"--theme\", choices=sorted(THEMES.keys()), default=\"default\")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print(\"error: width/height must be positive\", file=sys.stderr)
        return 1

    theme = THEMES[args.theme]
    t = escape(args.text)
    size = fit_font_size(args.text, args.width)
    y = args.height // 2
    print(f'<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{args.width}\" height=\"{args.height}\">')
    print(f'  <rect width=\"100%\" height=\"100%\" fill=\"{theme[\"bg\"]}\"/>')
    print(f'  <text x=\"20\" y=\"{y}\" fill=\"{theme[\"fg\"]}\" font-size=\"{size}\">{t}</text>')
    print(\"</svg>\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    s2 = """## Step 2: Keep output deterministic and validate theme

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    \"default\": {\"bg\": \"#111111\", \"fg\": \"#ffffff\"},
    \"invert\": {\"bg\": \"#ffffff\", \"fg\": \"#111111\"},
}


def fit_font_size(text: str, width: int, base: int = 32) -> int:
    if not text:
        return base
    max_chars = max(1, int((width - 40) / (base * 0.6)))
    if len(text) <= max_chars:
        return base
    scale = max_chars / len(text)
    return max(10, int(base * scale))


def main() -> int:
    p = argparse.ArgumentParser(prog=\"logo.py\")
    p.add_argument(\"text\")
    p.add_argument(\"--width\", type=int, default=300)
    p.add_argument(\"--height\", type=int, default=120)
    p.add_argument(\"--theme\", choices=sorted(THEMES.keys()), default=\"default\")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print(\"error: width/height must be positive\", file=sys.stderr)
        return 1

    theme = THEMES[args.theme]
    t = escape(args.text)
    size = fit_font_size(args.text, args.width)
    y = args.height // 2
    print(f'<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{args.width}\" height=\"{args.height}\">')
    print(f'  <rect width=\"100%\" height=\"100%\" fill=\"{theme[\"bg\"]}\"/>')
    print(f'  <text x=\"20\" y=\"{y}\" fill=\"{theme[\"fg\"]}\" font-size=\"{size}\">{t}</text>')
    print(\"</svg>\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
```
"""
    return s1 + "\n" + s2


def make_trace(problem_slug: str, persona: str) -> str:
    if problem_slug == "temperature-converter":
        body = temp_converter(persona)
    elif problem_slug == "word-frequency-counter":
        body = word_counter(persona)
    elif problem_slug == "todo-list-tui":
        body = todo_tui(persona)
    elif problem_slug == "ascii-art-poster":
        body = ascii_poster(persona)
    elif problem_slug == "interactive-fiction-engine":
        body = fiction_engine(persona)
    elif problem_slug == "conway-life-sim":
        body = conway_life(persona)
    elif problem_slug == "haiku-generator":
        body = haiku(persona)
    elif problem_slug == "maze-generator-solver":
        body = maze(persona)
    elif problem_slug == "svg-logo-generator":
        body = svg_logo(persona)
    else:
        raise ValueError(problem_slug)

    return header(persona, problem_slug) + body


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="generate_trace02.py")
    p.add_argument("--traces-root", type=Path, default=Path("traces"))
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv)

    root: Path = args.traces_root
    for prob in PROBLEMS:
        prob_dir = root / prob.slug
        if not prob_dir.exists():
            continue
        for persona in PERSONAS:
            persona_dir = prob_dir / persona
            if not persona_dir.exists():
                continue
            if not (persona_dir / "trace-01.md").exists():
                continue
            out = persona_dir / "trace-02.md"
            text = make_trace(prob.slug, persona)
            write(out, text, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv[1:]))
