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
