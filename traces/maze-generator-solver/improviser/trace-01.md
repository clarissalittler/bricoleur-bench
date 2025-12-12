# Trace 01 – Improviser (Maze Generator + Solver)

Spikes generation quickly, then adds solve/validation when the first maze is broken.

## Step 1: Generator only (accidentally makes ragged lines)

Snapshot: maze.py
```python
import random
import sys

w, h, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)

for y in range(h):
    row = []
    for x in range(w):
        row.append("." if rng.random() < 0.7 else "#")
    print("".join(row))
```

Notes: No S/E; solver can’t work; also wants a stable format and a solve command.

## Step 2: Add S/E and a solver (discover unsolvable mazes)

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


def gen(width: int, height: int, seed: int):
    rng = random.Random(seed)
    grid = [["."] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if rng.random() < 0.25:
                grid[y][x] = "#"
    grid[1][1] = "S"
    grid[height - 2][width - 2] = "E"
    return grid


def solve_length(grid):
    h = len(grid)
    w = len(grid[0])
    start = (1, 1)
    end = (w - 2, h - 2)
    q = deque([(start[0], start[1], 0)])
    seen = {start}
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                if grid[ny][nx] in (".", "E"):
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1))
    return None


def print_grid(grid):
    for row in grid:
        print("".join(row))


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("maze")
    args = p.parse_args()

    if args.cmd == "gen":
        print_grid(gen(args.width, args.height, args.seed))
        return 0
    else:
        grid = [list(l.rstrip("\n")) for l in open(args.maze).read().splitlines() if l.strip()]
        dist = solve_length(grid)
        if dist is None:
            print("error: unsolvable", file=sys.stderr)
            return 1
        print(f"path_length={dist}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Learns the hard way that random walls often produce unsolvable mazes.

## Step 3: Guarantee solvable by carving a path first

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


ALLOWED = {"#", ".", "S", "E"}


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise SystemExit("error: empty maze")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise SystemExit("error: ragged maze")
    grid = [list(l) for l in lines]
    for row in grid:
        for ch in row:
            if ch not in ALLOWED:
                raise SystemExit("error: unknown character in maze")
    return grid


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def solve_length(grid):
    start = find(grid, "S")
    end = find(grid, "E")
    if not start or not end:
        raise SystemExit("error: missing S or E")
    w = len(grid[0])
    h = len(grid)
    q = deque([(start[0], start[1], 0)])
    seen = {start}
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                if grid[ny][nx] in (".", "E"):
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1))
    return None


def gen(width: int, height: int, seed: int):
    rng = random.Random(seed)
    grid = [["#"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = "."

    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    path = {(sx, sy)}
    x, y = sx, sy
    while (x, y) != (ex, ey):
        if rng.random() < 0.5 and x < ex:
            x += 1
        elif y < ey:
            y += 1
        path.add((x, y))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.30:
                grid[y][x] = "#"

    grid[sy][sx] = "S"
    grid[ey][ex] = "E"
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))


def main() -> int:
    p = argparse.ArgumentParser(prog="maze.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("maze")
    args = p.parse_args()

    if args.cmd == "gen":
        print_grid(gen(args.width, args.height, args.seed))
        return 0

    grid = parse(args.maze)
    dist = solve_length(grid)
    if dist is None:
        print("error: unsolvable", file=sys.stderr)
        return 1
    print(f"path_length={dist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
