import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("--top", type=int, default=None)
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
for word, count in counts.most_common(args.top):
    print(f"{word}: {count}")
