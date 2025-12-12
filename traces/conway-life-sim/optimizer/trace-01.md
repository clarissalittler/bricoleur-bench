# Trace 01 – Optimizer (Conway’s Game of Life)

Baseline first; then reduce repeated bounds checks by precomputing neighbor offsets and keeping grids as lists.

## Step 1: Straightforward implementation

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
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    return raw


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
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

Notes: Accepts this as baseline; optional later optimization is switching to integer grids.

## Step 2: Keep internal grid as booleans (less string indexing)

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_grid(path: str) -> list[list[bool]]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    return [[ch == "#" for ch in line] for line in raw]


def render(grid: list[list[bool]]) -> str:
    return "\n".join("".join("#" if cell else "." for cell in row) for row in grid)


def step(grid: list[list[bool]]) -> list[list[bool]]:
    h = len(grid)
    w = len(grid[0])
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and grid[ny][nx]:
                    n += 1
            alive = grid[y][x]
            out[y][x] = (alive and n in (2, 3)) or ((not alive) and n == 3)
    return out


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern")
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1

    grid = parse_grid(args.pattern)
    print(render(grid))
    for _ in range(args.steps):
        print()
        grid = step(grid)
        print(render(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Validate characters and keep output stable

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_grid(path: str) -> list[list[bool]]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    for line in raw:
        for ch in line:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")
    return [[ch == "#" for ch in line] for line in raw]


def render(grid: list[list[bool]]) -> str:
    return "\n".join("".join("#" if cell else "." for cell in row) for row in grid)


def step(grid: list[list[bool]]) -> list[list[bool]]:
    h = len(grid)
    w = len(grid[0])
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and grid[ny][nx]:
                    n += 1
            alive = grid[y][x]
            out[y][x] = (alive and n in (2, 3)) or ((not alive) and n == 3)
    return out


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern")
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1

    grid = parse_grid(args.pattern)
    print(render(grid))
    for _ in range(args.steps):
        print()
        grid = step(grid)
        print(render(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
