# Trace 01 – Planner

A methodical path toward the converter. The student outlines steps, implements them in order, and validates along the way. Each checkpoint records what was verified before moving on.

## Plan
- Parse CLI arguments with mutually exclusive options for direction.
- Validate numeric input and reject missing direction.
- Output the converted value with unit label and sensible rounding.
- Guard against non-finite input (`nan`, `inf`) and document usage examples.

## Step 1: Skeleton with argparse and placeholders
Starts with structure and TODOs.

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
parser.add_argument("value")  # TODO: type=float
args = parser.parse_args()

# TODO: implement conversion logic
print(args)
```

Notes: Confirms the parser rejects missing direction. Leaves TODO to type the positional argument and to add helpers.

## Step 2: Add typing and basic conversion helpers
Implements conversion functions and enforces float input.

```python
import argparse

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()


def to_f(celsius: float) -> float:
    return celsius * 9/5 + 32


def to_c(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9

if args.to_f:
    result = to_f(args.value)
else:
    result = to_c(args.value)

print(result)
```

Notes: Tests with `--to-f 0` and `--to-c 32` produce expected numbers but without units. Plan update: "add output formatting".

## Step 3: Add formatting and friendlier errors
Formats output and adds a guard for NaN/inf input.

```python
import argparse
import math

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
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

Notes: Validation pass: `--to-f nan` now exits with a clear message. Output now shows units and two decimal places. Plan items 2–3 checked.

## Step 4: Document usage and edge cases
Adds short usage examples and confirms exit codes for bad inputs.

```
python convert.py --to-f 20    # -> 68.00F
python convert.py --to-c 451   # -> 232.78C
python convert.py --to-f nan   # exits with "Temperature must be a finite number" and status 1
python convert.py 10           # argparse error about missing direction
```

Notes: Plan complete; leaves a follow-up note to add unit tests in a future trace if needed.
