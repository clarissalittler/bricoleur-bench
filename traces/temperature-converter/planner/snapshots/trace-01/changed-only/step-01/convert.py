import argparse

parser = argparse.ArgumentParser(description="Convert temperatures")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--to-f", action="store_true", help="Celsius to Fahrenheit")
group.add_argument("--to-c", action="store_true", help="Fahrenheit to Celsius")
parser.add_argument("value")  # TODO: type=float
args = parser.parse_args()

# TODO: implement conversion logic
print(args)
