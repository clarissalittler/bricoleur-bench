# Trace 01 (Bricoleur)

### Step 1 — Quick skeleton
- Start `count_words.py` with a barebones `argparse` that expects `path` and optional `--top`.
- Hard-code a `Counter` pipeline; ignore apostrophes for now.
Snapshot: count_words.py
```python
import argparse
import re
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

with open(args.path) as fh:
    words = re.findall(r"[A-Za-z]+", fh.read().lower())
counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
```
Notes: Runs `python count_words.py sample.txt` and sees `"don't"` counted as `don` and `t`. Decides to keep internal apostrophes.

### Step 2 — Normalize apostrophes and empty file
- Adjusted regex to keep internal apostrophes but drop leading/trailing apostrophes.
- Added guard for empty file: if no words, exit cleanly without printing.
Snapshot: count_words.py
```python
import argparse
import re
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

with open(args.path) as fh:
    text = fh.read()

words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
if not words:
    raise SystemExit(0)

counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
```
- Checked `python count_words.py empty.txt` -> no output, exit 0.

### Step 3 — Friendly errors
- Wrapped file open in `try/except FileNotFoundError` with `sys.exit(1)` message.
- Added usage example to `ArgumentParser` description.
- Tested missing file: `python count_words.py nope.txt` now prints "file not found" and exits non-zero.

Snapshot: count_words.py
```python
import argparse
import re
import sys
from collections import Counter

parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

try:
    with open(args.path) as fh:
        text = fh.read()
except FileNotFoundError:
    print(f"file not found: {args.path}", file=sys.stderr)
    raise SystemExit(1)

words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
if not words:
    raise SystemExit(0)

counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
```

### Step 4 — Top-N clamp and formatting
- Ensured `--top 0` behaves like no output instead of crash (Counter handles slice).
- Formatted output as `word: count` for readability.
- Manual check with `--top 3` matched expectations; left TODO to add unit tests later.

Snapshot: count_words.py
```python
import argparse
import re
import sys
from collections import Counter

parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

try:
    with open(args.path) as fh:
        text = fh.read()
except FileNotFoundError:
    print(f"file not found: {args.path}", file=sys.stderr)
    raise SystemExit(1)

words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
if not words:
    raise SystemExit(0)

counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(f"{word}: {count}")
```
