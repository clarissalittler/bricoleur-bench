# Word Frequency Counter CLI

Goal: Build a Python script that reads a text file and prints word frequencies sorted by descending count.

## Requirements
- Accept an input file path and optionally a `--top N` limit.
- Normalize words by lowercasing and stripping punctuation.
- Treat apostrophes inside words (e.g., "don't") as part of the token, but strip surrounding punctuation.
- Handle empty files gracefully by reporting no results.
- Emit help text that shows a minimal usage example.

## Acceptance criteria
- Running `python count_words.py sample.txt` prints each word and count in descending frequency, one per line.
- Running with `--top 3` only prints the three most frequent words.
- Passing a missing file reports a clear error and non-zero exit status.
- An input containing only punctuation produces no output and exits successfully.

## Trace organization
- `bricoleur/` captures a quick-and-dirty path with early probing and iterative cleanup.
- `planner/` shows a checklist-driven implementation with checkpoints and test notes.
- `skeptic/` highlights a test-first, edge-case probing style with instrumentation.

Each trace narrates incremental edits, surprises, and verification steps to arrive at a reliable counter.
