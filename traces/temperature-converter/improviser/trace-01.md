# Trace 01 (Improviser)

### Step 1 — Rough CLI
- Copied argparse snippet from another script; added flags `--to-f` and `--to-c` plus positional `value`.
- Skipped validation and printed `float(value)` converted with inline formula.
- Ran `python convert.py --to-f 0` -> `32.0` works, but `--to-f --to-c` not blocked.

### Step 2 — Quick guardrails
- Added check to ensure exactly one direction flag; otherwise `parser.error("choose one conversion")`.
- Wrapped conversion in try/except `ValueError` to handle `abc`; exits non-zero with message.
- Tested `python convert.py --to-f abc` now prints error instead of stack trace.

### Step 3 — Formatting and samples
- Added formatted output with two decimals and unit suffix (e.g., `f"{result:.2f}F"`).
- Included examples in parser description to remind how to call the script.
- Confirmed `python convert.py --to-c 212` prints `100.00C`.

### Step 4 — Edge-case sweep
- Added rejection for `math.isfinite` to avoid `nan`/`inf` inputs.
- Noted TODO to support Kelvin later but deferred.
- Ran quick loop converting `-40` both ways to confirm symmetry; outputs match expectation.
