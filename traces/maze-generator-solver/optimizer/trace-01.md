# Trace 01 – Optimizer (Maze Generator + Solver)

Baseline correct BFS first; then reduces allocation and repeated scanning.

## Step 1: Baseline solver (scans for S/E with nested loops)

Snapshot: maze.py
```python
import sys
from collections import deque


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    return [list(l) for l in lines]


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def solve_length(grid):
    w = len(grid[0])
    h = len(grid)
    start = find(grid, "S")
    end = find(grid, "E")
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


grid = parse(sys.argv[1])
print("path_length=" + str(solve_length(grid)))
```

Notes: For large mazes, set lookups dominate; tries to use a boolean visited grid.

## Step 2: Use a 2D visited grid to reduce tuple hashing

Snapshot: maze.py
```python
import sys
from collections import deque


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    return [list(l) for l in lines]


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def solve_length(grid):
    w = len(grid[0])
    h = len(grid)
    start = find(grid, "S")
    end = find(grid, "E")
    visited = [[False] * w for _ in range(h)]
    q = deque([(start[0], start[1], 0)])
    visited[start[1]][start[0]] = True
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                if grid[ny][nx] in (".", "E"):
                    visited[ny][nx] = True
                    q.append((nx, ny, d + 1))
    return None


grid = parse(sys.argv[1])
print("path_length=" + str(solve_length(grid)))
```

Notes: Then adds CLI + generator later (keeps solver optimized).

## Step 3: Full CLI with generator (keeps solver internals)

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise SystemExit("error: empty maze")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise SystemExit("error: ragged maze")
    return [list(l) for l in lines]


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def solve_length(grid):
    w = len(grid[0])
    h = len(grid)
    start = find(grid, "S")
    end = find(grid, "E")
    if not start or not end:
        raise SystemExit("error: missing S or E")
    visited = [[False] * w for _ in range(h)]
    q = deque([(start[0], start[1], 0)])
    visited[start[1]][start[0]] = True
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                if grid[ny][nx] in (".", "E"):
                    visited[ny][nx] = True
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
