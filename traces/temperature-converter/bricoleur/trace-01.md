# Trace 01 – Bricoleur

A tinkering path toward a working converter script. The student tries to keep the program runnable after small tweaks, with occasional missteps and informal testing after each change.

## Step 1: Quick scaffold
Creates a minimal script with a single direction (C→F) and manual input parsing.

```python
value = float(input("Temp in C: "))
print(value * 9/5 + 32)
```

Notes: Works for happy path but no error handling or Fahrenheit support. First run with `0` prints `32.0`, which matches the mental check.

## Step 2: Adds Fahrenheit path but mixes formulas
Adds a flag prompt but accidentally reuses the same formula for both conversions.

```python
scale = input("convert to (c/f): ").strip().lower()
value = float(input("Temperature: "))

if scale == "f":
    print(value * 9/5 + 32)
elif scale == "c":
    print(value * 9/5 + 32)  # oops
else:
    print("unknown option")
```

Notes: Notices Celsius conversion is wrong after trying `scale=c` and seeing numbers go up. Leaves a sticky note: "need formula (F-32)*5/9".

## Step 3: Fixes Celsius conversion and adds basic validation
Switches the formula, guards against empty input, and keeps exceptions blunt.

```python
scale = input("convert to (c/f): ").strip().lower()
if not scale:
    raise SystemExit("Need a target scale")

try:
    value = float(input("Temperature: "))
except ValueError:
    raise SystemExit("Temperature must be a number")

if scale == "f":
    print(value * 9/5 + 32)
elif scale == "c":
    print((value - 32) * 5/9)
else:
    print("unknown option")
```

Notes: Happy path works; tests `scale=c` with `32` and gets `0.0`. Realizes this is clunky to reuse from the command line without prompts.

## Step 4: Copies logic into a script and forgets units in output
Moves to `argparse` for direct CLI use but prints bare numbers and allows both flags at once.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("value", type=float)
parser.add_argument("--to-f", action="store_true")
parser.add_argument("--to-c", action="store_true")
args = parser.parse_args()

if args.to_f:
    result = args.value * 9/5 + 32
elif args.to_c:
    result = (args.value - 32) * 5/9
else:
    raise SystemExit("Choose --to-f or --to-c")

print(result)
```

Notes: Manual tests:
- `python convert.py 10 --to-f` → `50.0` (good).
- `python convert.py 50 --to-c --to-f` silently prefers first branch—confusing.
- Output lacks unit suffix.

## Step 5: Introduces helpers and a bug when negating Fahrenheit
Extracts helper functions but inverts the subtraction incorrectly.

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures")
parser.add_argument("value", type=float)
parser.add_argument("--to-f", action="store_true")
parser.add_argument("--to-c", action="store_true")
args = parser.parse_args()


def to_f(celsius: float) -> float:
    return celsius * 9/5 + 32


def to_c(fahrenheit: float) -> float:
    return (32 - fahrenheit) * 5/9  # wrong order

if args.to_f:
    result = to_f(args.value)
elif args.to_c:
    result = to_c(args.value)
else:
    raise SystemExit("Choose --to-f or --to-c")

print(result)
```

Notes: Runs `python convert.py 32 --to-c` and gets `-0.0`, so suspects subtraction order. Scribbles "should be (fahrenheit - 32)" beside function.

## Step 6: Fixes helper and guards against double flags
Restores correct formula, adds mutually exclusive group, and starts formatting output.

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Convert Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Convert Fahrenheit to Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()


def to_f(celsius: float) -> float:
    return celsius * 9/5 + 32


def to_c(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9

if args.to_f:
    result = to_f(args.value)
    unit = "F"
else:
    result = to_c(args.value)
    unit = "C"

print(f"{result:.2f}{unit}")
```

Notes: Now `python convert.py --to-c 451` prints `232.78C`. Adds a TODO to reject `nan`/`inf` inputs.

## Step 7: Handles non-finite inputs and clarifies errors
Adds a finite check and clearer exit messages, plus an example for future self.

```python
import argparse
import math

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Convert Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Convert Fahrenheit to Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()


def to_f(celsius: float) -> float:
    return celsius * 9/5 + 32


def to_c(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9

if not math.isfinite(args.value):
    raise SystemExit("Temperature must be a finite number")

if args.to_f:
    result = to_f(args.value)
    unit = "F"
else:
    result = to_c(args.value)
    unit = "C"

print(f"{result:.2f}{unit}")
```

Notes: Quick probes:
- `python convert.py --to-f nan` now exits with the custom message.
- `python convert.py --to-f 0` prints `32.00F` as expected.

## Step 8: Final polish and examples
Adds short usage hints and keeps formatting consistent.

```
# Example runs
python convert.py --to-f 20    # 68.00F
python convert.py --to-c 212   # 100.00C
```

Trace ends with a working script plus guardrails; student is satisfied after verifying both directions and the non-finite check.
