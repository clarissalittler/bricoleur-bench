# Trace 01 – Debugger (Conway’s Game of Life)

Uses a known oscillator (blinker) as a reproduction target and adds probes for neighbor counts.

## Step 1: Wrong rule implementation (blinker doesn’t oscillate)

Snapshot: patterns/blinker.txt
```text
.....
..#..
..#..
..#..
.....
```

Snapshot: life.py
```python
import sys


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
            # bug: mistakenly keeps cells alive at n==4
            row.append("#" if (alive and n in (2, 3, 4)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


lines = [l.rstrip("\n") for l in open(sys.argv[1]).read().splitlines() if l.strip()]
print("\n".join(lines))
print()
print("\n".join(step(lines)))
```

Notes: Suspects the neighbor condition; adds a probe for the central cell.

## Step 2: Adds a probe (prints neighbor counts for a coordinate)

Snapshot: life.py
```python
import sys


def neighbor_count(lines: list[str], x: int, y: int) -> int:
    h = len(lines)
    w = len(lines[0])
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                n += 1
    return n


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = neighbor_count(lines, x, y)
            if (x, y) == (2, 2):
                print("debug center neighbors=", n)
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


lines = [l.rstrip("\n") for l in open(sys.argv[1]).read().splitlines() if l.strip()]
print("\n".join(lines))
print()
print("\n".join(step(lines)))
```

Notes: Probe confirms counts; fixes rule and adds CLI loop.

## Step 3: CLI `--steps` and stable output format

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
