# Trace 01 (Bricoleur)

### Step 1 — Quick skeleton
- Start `count_words.py` with a barebones `argparse` that expects `path` and optional `--top`.
- Hard-code a `Counter` pipeline; ignore punctuation for now.
```python
from collections import Counter
import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

with open(args.path) as fh:
    words = re.findall(r"[A-Za-z']+", fh.read().lower())
counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
```
- Ran `python count_words.py sample.txt` and saw output but apostrophes got split weirdly.

### Step 2 — Normalize apostrophes and empty file
- Adjusted regex to keep internal apostrophes but drop leading/trailing punctuation.
- Added guard for empty file: if no words, exit cleanly without printing.
```python
words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
```
- Checked `python count_words.py empty.txt` -> no output, exit 0.

### Step 3 — Friendly errors
- Wrapped file open in `try/except FileNotFoundError` with `sys.exit(1)` message.
- Added usage example to `ArgumentParser` description.
- Tested missing file: `python count_words.py nope.txt` now prints "file not found" and exits non-zero.

### Step 4 — Top-N clamp and formatting
- Ensured `--top 0` behaves like no output instead of crash (Counter handles slice).
- Formatted output as `word: count` for readability.
- Manual check with `--top 3` matched expectations; left TODO to add unit tests later.
