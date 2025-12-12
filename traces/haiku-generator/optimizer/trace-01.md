# Trace 01 – Optimizer (Haiku / Microfiction Generator)

Correct baseline first; then avoids repeated random choices and string joins for larger templates.

## Step 1: Baseline seeded generator

Snapshot: words/basic.txt
```text
river
stone
wind
quiet
lantern
paper
shadow
morning
night
echo
```

Snapshot: haiku.py
```python
import argparse
import random


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    if args.style == "micro":
        print(" ".join(rng.choice(words) for _ in range(10)).capitalize() + ".")
    else:
        for _ in range(3):
            print(" ".join(rng.choice(words) for _ in range(3)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Batch choice generation (fewer generator chains)

Snapshot: haiku.py
```python
import argparse
import random


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


def pick(rng: random.Random, words: list[str], n: int) -> list[str]:
    return [words[rng.randrange(len(words))] for _ in range(n)]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)

    if args.style == "micro":
        print(" ".join(pick(rng, words, 10)).capitalize() + ".")
        return 0

    for _ in range(3):
        print(" ".join(pick(rng, words, 3)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Add validation but keep hot path simple

Snapshot: haiku.py
```python
import argparse
import random
import sys


def read_words(path: str) -> list[str]:
    try:
        raw = [w.strip() for w in open(path).read().splitlines()]
    except FileNotFoundError:
        print(f"error: missing word list: {path}", file=sys.stderr)
        raise SystemExit(1)
    words = [w for w in raw if w]
    if not words:
        print("error: word list is empty", file=sys.stderr)
        raise SystemExit(1)
    return words


def pick(rng: random.Random, words: list[str], n: int) -> list[str]:
    return [words[rng.randrange(len(words))] for _ in range(n)]


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)

    if args.style == "micro":
        print(" ".join(pick(rng, words, 10)).capitalize() + ".")
        return 0

    for _ in range(3):
        print(" ".join(pick(rng, words, 3)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
