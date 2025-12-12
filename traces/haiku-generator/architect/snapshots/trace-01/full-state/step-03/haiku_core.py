from __future__ import annotations

import random


def gen_haiku(rng: random.Random, words: list[str], *, words_per_line: int = 3) -> str:
    return "\n".join(" ".join(rng.choice(words) for _ in range(words_per_line)) for _ in range(3)) + "\n"


def gen_micro(rng: random.Random, words: list[str], *, sentence_words: int = 6) -> str:
    a = " ".join(rng.choice(words) for _ in range(sentence_words)).capitalize() + "."
    b = " ".join(rng.choice(words) for _ in range(sentence_words)).capitalize() + "."
    return a + " " + b + "\n"
