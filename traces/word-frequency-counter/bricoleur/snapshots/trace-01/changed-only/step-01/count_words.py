import argparse
import re
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--top", type=int, default=None)
args = parser.parse_args()

with open(args.path) as fh:
    words = re.findall(r"[A-Za-z]+", fh.read().lower())
counts = Counter(words)
for word, count in counts.most_common(args.top):
    print(word, count)
