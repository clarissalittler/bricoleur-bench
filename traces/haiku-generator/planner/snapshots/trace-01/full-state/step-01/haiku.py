import random


def gen_haiku(rng: random.Random, words: list[str]) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(3)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str]) -> str:
    a = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(6)).capitalize() + "."
    return a + " " + b + "\n"
