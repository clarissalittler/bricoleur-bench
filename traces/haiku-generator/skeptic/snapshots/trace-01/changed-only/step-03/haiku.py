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
