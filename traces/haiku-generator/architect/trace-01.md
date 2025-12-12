# Trace 01 – Architect (Haiku / Microfiction Generator)

Separates template logic from CLI for easy future “styles”.

## Step 1: Core module (templates)

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

Snapshot: haiku_core.py
```python
from __future__ import annotations

import random


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"
```

## Step 2: CLI wrapper with deterministic seed

Snapshot: haiku.py
```python
import argparse
import random
import sys

from haiku_core import gen_haiku, gen_micro


def read_words(path: str) -> list[str]:
    raw = [w.strip() for w in open(path).read().splitlines()]
    words = [w for w in raw if w]
    if not words:
        raise ValueError("word list is empty")
    return words


def main() -> int:
    p = argparse.ArgumentParser(prog="haiku.py")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--style", choices=["haiku", "micro"], default="haiku")
    p.add_argument("words")
    args = p.parse_args()

    try:
        words = read_words(args.words)
    except FileNotFoundError:
        print(f"error: missing word list: {args.words}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    rng = random.Random(args.seed)
    out = gen_micro(rng, words) if args.style == "micro" else gen_haiku(rng, words)
    print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Keep defaults stable; add room for future themes

Snapshot: haiku_core.py
```python
from __future__ import annotations

import random


def gen_haiku(rng: random.Random, words: list[str], *, words_per_line: int = 3) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(words_per_line)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str], *, sentence_words: int = 6) -> str:
    a = " ".join(rng.choice(words) for _ in range(sentence_words)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(sentence_words)).capitalize() + "."
    return a + " " + b + "\n"
```
