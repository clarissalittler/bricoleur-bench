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
