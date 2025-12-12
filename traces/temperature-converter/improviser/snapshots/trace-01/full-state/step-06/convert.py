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
