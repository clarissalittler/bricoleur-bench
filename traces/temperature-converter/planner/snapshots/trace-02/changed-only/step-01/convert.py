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
