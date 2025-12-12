import argparse
import re
import sys
from collections import Counter

parser = argparse.ArgumentParser(
    description="Count word frequencies.\n\nExample:\n  python count_words.py sample.txt --top 5",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

try:
    with open(args.path) as fh:
        text = fh.read()
except FileNotFoundError:
    print(f"file not found: {args.path}", file=sys.stderr)
    raise SystemExit(1)

words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
if not words:
    raise SystemExit(0)

counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(f"{word}: {count}")
