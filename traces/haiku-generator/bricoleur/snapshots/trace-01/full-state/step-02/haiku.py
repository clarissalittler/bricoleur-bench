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
