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
