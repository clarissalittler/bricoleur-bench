# Trace 01 (Planner)

### Plan
- Define CLI contract: `path`, optional `--top`, helpful description and `--help` example.
- Build tokenizer that keeps internal apostrophes and ignores punctuation-only tokens.
- Implement counting and sorting; format as `word: count`.
- Add validation: missing file, invalid `--top`, empty files.
- Smoke-test with sample files and edge cases.

### Step 1 — CLI scaffold
- Wrote `argparse` setup with description including `python count_words.py sample.txt --top 5`.
- Added `type=int` for `--top` and rejected negatives with a custom error message.
- Inserted placeholder `print("TODO")` to verify argument parsing; confirmed `--help` text shows example.

### Step 2 — Tokenization helper
- Added `def tokenize(text):` using regex `r"[A-Za-z']+"` then `strip("'" )` to drop leading/trailing apostrophes.
- Added docstring noting apostrophes inside words are preserved.
- Quick unit-ish check inside `__main__` with sample string `"Don't stop, can't stop"` to see `dont`, `stop`, `cant`.

### Step 3 — Counting and output
- Wired tokenizer into a `Counter` pipeline; used `most_common(args.top)` to handle optional top-N.
- Formatted lines with `f"{word}: {count}"` and kept stdout only, no extra whitespace.
- Verified output ordering with a small fixture file containing repeated words.

### Step 4 — Validation and exit codes
- Wrapped file open in `try/except FileNotFoundError` to emit `sys.exit("missing file: ...")`.
- Guarded against `args.top is not None and args.top < 1` with `parser.error("--top must be positive")`.
- Added early return when no tokens are produced; prints nothing and exits 0.

### Step 5 — Smoke tests
- `python count_words.py fixtures/lorem.txt --top 3` matched manual expectations.
- `python count_words.py fixtures/empty.txt` produced no lines and exit 0.
- `python count_words.py missing.txt` printed clear error and exit status 1.
- Left TODOs: move tokenizer to separate module and add pytest cases for punctuation-heavy lines.
