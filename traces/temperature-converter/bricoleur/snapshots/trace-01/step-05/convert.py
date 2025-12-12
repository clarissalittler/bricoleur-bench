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
