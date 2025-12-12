# Trace 01 – Skeptic (Conway’s Game of Life)

Pins the blinker behavior with a tiny harness before writing the full CLI.

## Step 1: Harness first (blinker should flip)

Snapshot: patterns/blinker.txt
```text
.....
..#..
..#..
..#..
.....
```

Snapshot: harness.py
```python
import subprocess
import sys

run = subprocess.run(
    [sys.executable, "life.py", "--steps", "1", "patterns/blinker.txt"],
    text=True,
    capture_output=True,
)
assert run.returncode == 0
out = run.stdout.strip().splitlines()
assert len(out) > 0
```

Notes: Fails because `life.py` doesn’t exist.

## Step 2: Minimal life implementation to satisfy shape (no validation)

Snapshot: life.py
```python
import argparse


def parse_lines(path: str) -> list[str]:
    return [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                        n += 1
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern")
    args = p.parse_args()
    lines = parse_lines(args.pattern)
    print("\n".join(lines))
    for _ in range(args.steps):
        print()
        lines = step(lines)
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Harness passes (shape), now add validation and a stricter harness later.

## Step 3: Add validation and negative-step error

Snapshot: life.py
```python
import argparse
import sys


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    for l in raw:
        for ch in l:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")
    return raw


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                        n += 1
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern")
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1

    lines = parse_lines(args.pattern)
    print("\n".join(lines))
    for _ in range(args.steps):
        print()
        lines = step(lines)
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
