# Haiku / Microfiction Generator

Goal: Build a Python CLI that generates short poems (or microfiction) from word lists.

This is intentionally creativity-friendly, but must support deterministic generation via a seed so automated feedback systems can compare outputs.

## Requirements
- `python haiku.py --seed N words.txt` prints a generated poem and exits 0.
- The same seed and same word list produce the same output.
- Provide `--style haiku|micro` (default `haiku`) where:
  - `haiku` prints 3 lines
  - `micro` prints 1–3 sentences
- Validate that the word list file is readable and non-empty.

## Word list format
One word per line. Blank lines are ignored.

See `words/basic.txt` for a small starter set.

## Acceptance criteria (determinism + shape)
- Running twice with the same seed yields identical output.
- `--style haiku` prints exactly 3 lines.
- Missing word list exits non-zero with a clear error.

## Creative extensions (optional)
- Add optional parts-of-speech tags in the word file and richer templates.
- Add `--meter` checks or syllable heuristics (keep a simple default).
- Add `--theme` that biases word selection.

## Trace organization
Common student missteps: non-determinism, accidental global RNG state, and drifting output formats.
