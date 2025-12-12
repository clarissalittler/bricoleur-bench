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
