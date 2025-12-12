# Trace 01 – Improviser (Haiku / Microfiction Generator)

Spikes a few templates, then enforces determinism and a stable output shape.

## Step 1: Hard-coded template

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
import sys

words = [w.strip() for w in open(sys.argv[1]).read().splitlines() if w.strip()]
print(words[0], words[1], words[2])
print(words[3], words[4], words[5])
print(words[6], words[7], words[8])
```

Notes: Not very interesting; wants randomness, but acceptance wants deterministic `--seed`.

## Step 2: Seeded RNG + style flag

Snapshot: haiku.py
```python
import argparse
import random


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


def choose(rng: random.Random, words: list[str], n: int) -> str:
    return " ".join(rng.choice(words) for _ in range(n))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    if args.style == "micro":
        print(choose(rng, words, 8).capitalize() + ".")
    else:
        print(choose(rng, words, 3))
        print(choose(rng, words, 3))
        print(choose(rng, words, 3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Output now repeats for the same seed.

## Step 3: Make errors clear and keep formatting stable

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


def choose(rng: random.Random, words: list[str], n: int) -> str:
    return " ".join(rng.choice(words) for _ in range(n))


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)

    if args.style == "micro":
        print(choose(rng, words, 8).capitalize() + ".")
        return 0

    for _ in range(3):
        print(choose(rng, words, 3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
