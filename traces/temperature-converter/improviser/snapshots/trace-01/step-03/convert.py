import argparse

parser = argparse.ArgumentParser(description="Convert temperatures.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius → Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit → Celsius")
parser.add_argument("value", type=float, help="Temperature to convert")
args = parser.parse_args()

if args.to_f:
    result = args.value * 9 / 5 + 32
else:
    result = (args.value - 32) * 5 / 9

print(result)
