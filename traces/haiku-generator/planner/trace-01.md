# Trace 01 – Planner (Haiku / Microfiction Generator)

## Plan
- Enforce determinism with `--seed`.
- Validate word list file and non-empty content.
- Keep output shape strict per style (`haiku`=3 lines; `micro`=1 paragraph).

## Step 1: Core generator functions

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


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"
```

## Step 2: CLI with deterministic seed

Snapshot: haiku.py
```python
import argparse
import random


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"


def read_words(path: str) -> list[str]:
    return [w.strip() for w in open(path).read().splitlines() if w.strip()]


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

## Step 3: Validation and clear errors

Snapshot: haiku.py
```python
import argparse
import random
import sys


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"


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
