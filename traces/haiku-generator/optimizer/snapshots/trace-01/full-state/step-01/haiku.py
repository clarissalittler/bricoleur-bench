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
