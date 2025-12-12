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
