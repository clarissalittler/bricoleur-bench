import argparse
import re
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

with open(args.path) as fh:
    text = fh.read()

words = [w.strip("'") for w in re.findall(r"[A-Za-z']+", text.lower())]
words = [w for w in words if w]
if not words:
    raise SystemExit(0)

counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
