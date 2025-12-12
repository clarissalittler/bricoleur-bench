# Trace 01 – Skeptic (Haiku / Microfiction Generator)

Pins determinism and output shape with a harness first.

## Step 1: Harness first (same seed => same output)

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

Snapshot: harness.py
```python
import subprocess
import sys

cmd = [sys.executable, "haiku.py", "--seed", "123", "--style", "haiku", "words/basic.txt"]
a = subprocess.run(cmd, text=True, capture_output=True)
b = subprocess.run(cmd, text=True, capture_output=True)
assert a.returncode == 0
assert b.returncode == 0
assert a.stdout == b.stdout
assert len(a.stdout.strip().splitlines()) == 3
```

Notes: Fails because `haiku.py` doesn’t exist.

## Step 2: Minimal deterministic implementation

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

    if args.style == "haiku":
        for _ in range(3):
            print(" ".join(rng.choice(words) for _ in range(3)))
        return 0

    print(" ".join(rng.choice(words) for _ in range(10)).capitalize() + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Harness passes; adds validation next.

## Step 3: Validation for missing/empty word lists

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


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    words = read_words(args.words)
    rng = random.Random(args.seed)

    if args.style == "haiku":
        for _ in range(3):
            print(" ".join(rng.choice(words) for _ in range(3)))
        return 0

    print(" ".join(rng.choice(words) for _ in range(10)).capitalize() + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
