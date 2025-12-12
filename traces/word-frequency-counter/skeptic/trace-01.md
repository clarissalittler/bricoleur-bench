# Trace 01 (Skeptic)

### Baseline hypothesis
- Start from failing tests to outline behavior. Drafted checklist:
  - Missing file -> non-zero with error.
  - Empty file -> exit 0, no lines.
  - Punctuation-only -> no tokens.
  - Apostrophes internal -> kept.

### Step 1 — Red tests
- Wrote quick harness in `scratch/test_inputs.py` using `tempfile` to create fixtures.
- Asserted that running `python count_words.py --top 2` on `''` returns exit 0 and empty stdout (currently failed because script missing).
- Captured failure outputs to refine messages later.

### Step 2 — Minimal implementation
- Added `count_words.py` with `argparse` and `Path` open wrapped in `try/except FileNotFoundError`.
- Implemented `tokenize` using `re.findall(r"[A-Za-z']+")` then `strip("'")`; filtered empties.
- Added guard: if tokens empty, `sys.exit(0)` without printing.
- Re-ran harness: empty and punctuation-only cases now pass; missing file still failing on message wording.

### Step 3 — Tightening assertions
- Adjusted error path to `sys.exit("missing file: ...")` and updated test expectation accordingly.
- Added explicit check that `--top` rejects 0 or negatives via `argparse.ArgumentTypeError` helper.
- Introduced timing log for large files (`print("scanned", len(text), "chars", file=sys.stderr)`) guarded by `--debug` flag.

### Step 4 — Confidence sweep
- Added fixture with contractions to ensure `don't` -> `dont` not `don`.
- Verified ordering of ties remains deterministic via `most_common` (stable in Counter); noted in tests.
- Left TODO: integrate `pytest` and redirect stderr in assertions; current harness uses `subprocess.run` with check on `returncode`.
