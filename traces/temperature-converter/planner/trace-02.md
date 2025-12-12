# Trace 02 – Planner (temperature-converter)

## Step 1: Baseline works; tighten UX

Snapshot: convert.py
```python
import argparse
import math
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Convert temperatures.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
    group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
    parser.add_argument("value", type=float, help="Temperature to convert")
    args = parser.parse_args()

    if not math.isfinite(args.value):
        print("error: temperature must be finite", file=sys.stderr)
        return 1

    if args.to_f:
        result = args.value * 9 / 5 + 32
        unit = "F"
    else:
        result = (args.value - 32) * 5 / 9
        unit = "C"

    print(f"{result:.2f}{unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Better help + clearer errors

Snapshot: convert.py
```python
import argparse
import math
import sys


def finite_float(raw: str) -> float:
    try:
        value = float(raw)
    except ValueError as e:
        raise argparse.ArgumentTypeError("value must be a number") from e
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError("value must be finite")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Convert temperatures.

Examples:
  python convert.py --to-f 0
  python convert.py --to-c 212",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
    group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
    parser.add_argument("value", type=finite_float, help="Temperature to convert")
    args = parser.parse_args()

    if args.to_f:
        result = args.value * 9 / 5 + 32
        unit = "F"
    else:
        result = (args.value - 32) * 5 / 9
        unit = "C"

    print(f"{result:.2f}{unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
