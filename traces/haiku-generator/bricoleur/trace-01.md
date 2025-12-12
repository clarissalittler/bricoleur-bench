# Trace 01 – Bricoleur (Haiku / Microfiction Generator)

Starts with “random words go brrr”, then remembers determinism and output shape constraints.

## Step 1: Quick random poem (not deterministic)

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
    print(" ".join(random.choice(words) for _ in range(3)))
```

Notes: Runs twice and gets different outputs; acceptance wants `--seed`.

## Step 2: Add seed and style switch (micro vs haiku)

Snapshot: haiku.py
```python
import argparse
import random


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    if args.style == "micro":
        print(gen_micro(rng, words), end="")
    else:
        print(gen_haiku(rng, words), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Now the same seed repeats output.

## Step 3: Validate word list is non-empty and errors are clear

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


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    out = gen_micro(rng, words) if args.style == "micro" else gen_haiku(rng, words)
    print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
