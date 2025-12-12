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
