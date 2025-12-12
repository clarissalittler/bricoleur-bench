import argparse
import re
import sys
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z']+")


def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    tokens = [t.strip("'") for t in raw]
    return [t for t in tokens if t]


def main() -> int:
    p = argparse.ArgumentParser(prog="count_words.py")
    p.add_argument("path", type=Path)
    p.add_argument("--top", type=int, default=None)
    args = p.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"missing file: {args.path}", file=sys.stderr)
        return 1

    tokens = tokenize(text)
    if not tokens:
        return 0

    counts = Counter(tokens)
    items = list(counts.items())
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        items = items[: args.top]
    for word, count in items:
        print(f"{word}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
