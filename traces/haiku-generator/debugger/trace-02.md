# Trace 02 – Debugger (haiku-generator)

## Step 1: Add optional theme word bias

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


def biased_choice(rng: random.Random, words: list[str], theme: str | None) -> str:
    if not theme:
        return rng.choice(words)
    themed = [w for w in words if theme.lower() in w.lower()]
    pool = themed if themed else words
    return rng.choice(pool)


def gen_haiku(rng: random.Random, words: list[str], theme: str | None) -> str:
    return "\n".join(" ".join(biased_choice(rng, words, theme) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str], theme: str | None) -> str:
    a = " ".join(biased_choice(rng, words, theme) for _ in range(8)).capitalize() + "."
    return a + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("--theme", default=None)
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    out = gen_micro(rng, words, args.theme) if args.style == "micro" else gen_haiku(rng, words, args.theme)
    print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Make output shape stricter for micro style

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


def biased_choice(rng: random.Random, words: list[str], theme: str | None) -> str:
    if not theme:
        return rng.choice(words)
    themed = [w for w in words if theme.lower() in w.lower()]
    pool = themed if themed else words
    return rng.choice(pool)


def gen_haiku(rng: random.Random, words: list[str], theme: str | None) -> str:
    return "\n".join(" ".join(biased_choice(rng, words, theme) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str], theme: str | None) -> str:
    sentence = " ".join(biased_choice(rng, words, theme) for _ in range(10)).capitalize() + "."
    return sentence + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("--theme", default=None)
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)
    if args.style == "micro":
        print(gen_micro(rng, words, args.theme), end="")
        return 0
    print(gen_haiku(rng, words, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
