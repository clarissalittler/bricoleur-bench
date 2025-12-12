# Trace 01 – Debugger (Haiku / Microfiction Generator)

Targets two bugs: (1) output not deterministic, (2) haiku style doesn’t produce exactly 3 lines.

## Step 1: Repro nondeterminism

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
import random
import sys

words = [w.strip() for w in open(sys.argv[1]).read().splitlines() if w.strip()]
for _ in range(3):
    print(random.choice(words))
```

Notes: Runs twice and gets different outputs; adds `--seed` and a probe.

## Step 2: Add seed and a quick “same-seed” probe

Snapshot: haiku.py
```python
import argparse
import random


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)

    a = [rng.choice(words) for _ in range(3)]
    rng2 = random.Random(args.seed)
    b = [rng2.choice(words) for _ in range(3)]
    if a != b:
        raise SystemExit("debug: seed not deterministic")

    for line in a:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Determinism is good now; implements `--style` and ensures line counts.

## Step 3: Style handling + validation

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


def choose_words(rng: random.Random, words: list[str], n: int) -> str:
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
        print(choose_words(rng, words, 8).capitalize() + ".")
        return 0

    for _ in range(3):
        print(choose_words(rng, words, 3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
