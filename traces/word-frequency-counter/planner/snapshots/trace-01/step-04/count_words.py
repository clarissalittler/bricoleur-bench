import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return n


def tokenize(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw_tokens]
    return [t for t in tokens if t]


def format_counts(counts: Counter[str], top: int | None) -> list[tuple[str, int]]:
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    return items if top is None else items[:top]


parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=positive_int, default=None)
args = parser.parse_args()

try:
    text = args.path.read_text()
except FileNotFoundError:
    print(f"missing file: {args.path}", file=sys.stderr)
    raise SystemExit(1)

tokens = tokenize(text)
if not tokens:
    raise SystemExit(0)

counts = Counter(tokens)
for word, count in format_counts(counts, args.top):
    print(f"{word}: {count}")
