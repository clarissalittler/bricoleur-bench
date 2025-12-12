# Trace 01 (Planner)

Methodical: defines the contract, then fills in helpers with quick verification notes.

## Plan
- Define CLI contract: `path`, optional `--top`, helpful description and `--help` example.
- Build tokenizer that keeps internal apostrophes and ignores punctuation-only tokens.
- Implement counting and sorting; format as `word: count`.
- Add validation: missing file, invalid `--top`, empty files.
- Smoke-test with sample files and edge cases.

## Step 1: CLI scaffold

Snapshot: count_words.py

```python
import argparse
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

raise SystemExit(0)
```

Notes: Runs `python count_words.py --help` to confirm the example is visible and `--top 0` is rejected by argparse.

## Step 2: Tokenizer helper

Keeps internal apostrophes (e.g., `don't`) but strips leading/trailing apostrophes from weird tokens.

```python
import re


def tokenize(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw_tokens]
    return [t for t in tokens if t]
```

Notes: Quick mental check: `"Don't stop, can't stop"` should tokenize to `["don't", "stop", "can't", "stop"]`.

Snapshot: count_words.py
```python
import argparse
import re
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


def tokenize(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw_tokens]
    return [t for t in tokens if t]


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

raise SystemExit(0)
```

## Step 3: Counting + deterministic sorting

Uses explicit sorting to keep ties deterministic (descending count, then alphabetical).

```python
from collections import Counter


def format_counts(counts: Counter[str], top: int | None) -> list[tuple[str, int]]:
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    return items if top is None else items[:top]
```

Snapshot: count_words.py
```python
import argparse
import re
from collections import Counter
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


def tokenize(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw_tokens]
    return [t for t in tokens if t]


def format_counts(counts: Counter[str], top: int | None) -> list[tuple[str, int]]:
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    return items if top is None else items[:top]


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

raise SystemExit(0)
```

## Step 4: Wiring and validation

`count_words.py`

```python
import sys

try:
    text = args.path.read_text()
except FileNotFoundError:
    print(f"missing file: {args.path}", file=sys.stderr)
    raise SystemExit(1)

tokens = tokenize(text)
if not tokens:
    raise SystemExit(0)

counts = Counter(tokens)
for word, count in format_counts(counts, args.top):
    print(f"{word}: {count}")
```

Notes: Ensures punctuation-only input produces no output and exits successfully.

Snapshot: count_words.py
```python
import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


def tokenize(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw_tokens]
    return [t for t in tokens if t]


def format_counts(counts: Counter[str], top: int | None) -> list[tuple[str, int]]:
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    return items if top is None else items[:top]


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

try:
    text = args.path.read_text()
except FileNotFoundError:
    print(f"missing file: {args.path}", file=sys.stderr)
    raise SystemExit(1)

tokens = tokenize(text)
if not tokens:
    raise SystemExit(0)

counts = Counter(tokens)
for word, count in format_counts(counts, args.top):
    print(f"{word}: {count}")
```

## Step 5: Smoke tests (manual)

- `python count_words.py sample.txt` prints `word: count` lines, descending by count.
- `python count_words.py sample.txt --top 3` prints only 3 lines.
- `python count_words.py missing.txt` prints a clear error and exits non-zero.
- A file containing only punctuation prints nothing and exits 0.
