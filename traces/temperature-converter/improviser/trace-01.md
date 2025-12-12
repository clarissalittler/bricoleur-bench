# Trace 01 – Improviser

An improvising path: quick spike → a little cleanup → another spike → consolidate. The student bounces between “get it working” and “make it pleasant”.

## Step 1: Fast CLI (works, but sloppy)

Snapshot: convert.py

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--to-f", action="store_true")
parser.add_argument("--to-c", action="store_true")
parser.add_argument("value")  # leaving as string for now
args = parser.parse_args()

value = float(args.value)
if args.to_f:
    print(value * 9 / 5 + 32)
elif args.to_c:
    print((value - 32) * 5 / 9)
else:
    print("pick --to-f or --to-c")
```

Notes: `python convert.py --to-f 0` prints `32.0`. Tries `python convert.py --to-f --to-c 0` and realizes it silently picks the first branch.

## Step 2: Quick guardrails (slightly over-corrects)

Tries to “just error out” when flags are wrong.

Snapshot: convert.py

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--to-f", action="store_true")
parser.add_argument("--to-c", action="store_true")
parser.add_argument("value")  # leaving as string for now
args = parser.parse_args()

if args.to_f == args.to_c:
    raise SystemExit("choose exactly one of --to-f / --to-c")

value = float(args.value)
if args.to_f:
    result = value * 9 / 5 + 32
else:
    result = (value - 32) * 5 / 9

print(result)
```

Notes: This blocks both “none chosen” and “both chosen” with the same message. Acceptable, but not great UX.

## Step 3: Argparse does the exclusive-flag job

Refactor: let argparse enforce the contract.

Snapshot: convert.py

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()

if args.to_f:
    result = args.value * 9 / 5 + 32
else:
    result = (args.value - 32) * 5 / 9

print(result)
```

Notes: Now `python convert.py 10` shows an argparse error about missing one of `--to-f/--to-c`, and `--to-f --to-c` is rejected automatically.

## Step 4: Formatting (forgets units once)

Adds nicer output, but initially prints only the number.

Snapshot: convert.py

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()

if args.to_f:
    result = args.value * 9 / 5 + 32
    unit = "F"
else:
    result = (args.value - 32) * 5 / 9
    unit = "C"

print(f"{result:.2f}{unit}")
```

## Step 5: Reject non-finite inputs

Adds a quick edge-case sweep after noticing `float("nan")` parses cleanly.

Snapshot: convert.py

```python
import argparse
import math

parser = argparse.ArgumentParser(description="Convert temperatures.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()

if not math.isfinite(args.value):
    raise SystemExit("Temperature must be a finite number")

if args.to_f:
    result = args.value * 9 / 5 + 32
    unit = "F"
else:
    result = (args.value - 32) * 5 / 9
    unit = "C"

print(f"{result:.2f}{unit}")
```

Notes: `python convert.py --to-f nan` now exits non-zero with a readable message.

## Step 6: Examples in help output

Adds examples so the next run doesn’t require reading source.

Snapshot: convert.py

```python
import argparse
import math

parser = argparse.ArgumentParser(
    description="Convert temperatures.\n\nExamples:\n  python convert.py --to-f 0\n  python convert.py --to-c 212",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()

if not math.isfinite(args.value):
    raise SystemExit("Temperature must be a finite number")

if args.to_f:
    result = args.value * 9 / 5 + 32
    unit = "F"
else:
    result = (args.value - 32) * 5 / 9
    unit = "C"

print(f"{result:.2f}{unit}")
```

Final spot-checks:
- `python convert.py --to-f 0` → `32.00F`
- `python convert.py --to-c 212` → `100.00C`
- `python convert.py --to-c -40` → `-40.00C` (the “fun symmetry” check)
