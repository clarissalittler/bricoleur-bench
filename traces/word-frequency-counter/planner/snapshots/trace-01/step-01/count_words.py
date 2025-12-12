import argparse
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

raise SystemExit(0)
