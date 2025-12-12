# Trace 02 – Bricoleur (word-frequency-counter)

## Step 1: Deterministic ordering for ties

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
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


def main() -> int:
    p = argparse.ArgumentParser(prog="count_words.py")
    p.add_argument("path", type=Path)
    p.add_argument("--top", type=int, default=None)
    args = p.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"missing file: {args.path}", file=sys.stderr)
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
        print(f"{word}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Slightly broader tokenization (keeps default stable)

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
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


def positive_int(raw: str) -> int:
    try:
        n = int(raw)
    except ValueError as e:
        raise argparse.ArgumentTypeError("--top must be an integer") from e
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be positive")
    return n


def main() -> int:
    p = argparse.ArgumentParser(
        prog="count_words.py",
        description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("path", type=Path)
    p.add_argument("--top", type=positive_int, default=None)
    args = p.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"missing file: {args.path}", file=sys.stderr)
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
        print(f"{word}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
