# Trace 01 (Skeptic)

### Baseline hypothesis
- Start from failing tests to outline behavior. Drafted checklist:
  - Missing file -> non-zero with error.
  - Empty file -> exit 0, no lines.
  - Punctuation-only -> no tokens.
  - Apostrophes internal -> kept.

## Step 1: Red tests (inline harness)

Instead of “real tests”, the student writes a tiny driver script to force concrete expectations.

Snapshot: harness.py

```python
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "count_words.py", *args], text=True, capture_output=True)


def write_tmp(contents: str) -> Path:
    f = tempfile.NamedTemporaryFile("w+", delete=False)
    f.write(contents)
    f.flush()
    return Path(f.name)


empty = write_tmp("")
punct = write_tmp("!!! ... ---")
contractions = write_tmp("Don't stop. Can't stop.")

assert run([str(empty)]).returncode == 0
assert run([str(empty)]).stdout == ""

assert run([str(punct)]).returncode == 0
assert run([str(punct)]).stdout == ""

missing = run(["nope-does-not-exist.txt"])
assert missing.returncode != 0
assert "missing file" in (missing.stderr + missing.stdout).lower()
```

Notes: Everything fails initially because `count_words.py` doesn’t exist yet.

## Step 2: Minimal implementation (make the harness pass)

Snapshot: count_words.py

```python
import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=int, default=None)
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
for word, count in counts.most_common(args.top):
    print(f"{word}: {count}")
```

Notes: Re-runs the harness; empty and punctuation-only now pass. “Missing file” message now matches.

## Step 3: Tighten `--top` and add a debug hook

Adds a stricter type for `--top` so `--top 0` is rejected up front.

```python
def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n

parser.add_argument("--top", type=positive_int, default=None)
parser.add_argument("--debug", action="store_true")
```

And optional instrumentation:

```python
if args.debug:
    print(f"debug: scanned {len(text)} chars", file=sys.stderr)
```

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
    raw = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

try:
    text = args.path.read_text()
except FileNotFoundError:
    print(f"missing file: {args.path}", file=sys.stderr)
    raise SystemExit(1)

if args.debug:
    print(f"debug: scanned {len(text)} chars", file=sys.stderr)

tokens = tokenize(text)
if not tokens:
    raise SystemExit(0)

counts = Counter(tokens)
for word, count in counts.most_common(args.top):
    print(f"{word}: {count}")
```

## Step 4: Confidence sweep (contractions + tie ordering)

Adjusts expectations: apostrophes inside words are preserved, so `"Don't"` should count as `"don't"` (not `dont`).

Also notices `Counter.most_common()` doesn’t specify tie-breaking, so changes to deterministic sort:

```python
items = list(counts.items())
items.sort(key=lambda kv: (-kv[1], kv[0]))
items = items if args.top is None else items[: args.top]
for word, count in items:
    print(f"{word}: {count}")
```

Notes: Updates the harness to assert exact output lines only when ties are not present (or uses the deterministic sort so assertions are stable).

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
    raw = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

try:
    text = args.path.read_text()
except FileNotFoundError:
    print(f"missing file: {args.path}", file=sys.stderr)
    raise SystemExit(1)

if args.debug:
    print(f"debug: scanned {len(text)} chars", file=sys.stderr)

tokens = tokenize(text)
if not tokens:
    raise SystemExit(0)

counts = Counter(tokens)
items = list(counts.items())
items.sort(key=lambda kv: (-kv[1], kv[0]))
if args.top is not None:
    items = items[: args.top]

for word, count in items:
    print(f"{word}: {count}")
```
