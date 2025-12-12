# Trace 01 – Bricoleur (Maze Generator + Solver)

Starts by solving first (because it feels simpler), then bolts on generation.

## Step 1: Parser + BFS solver (no generator yet)

Snapshot: maze.py
```python
import sys
from collections import deque


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise SystemExit("error: ragged maze")
    grid = [list(l) for l in lines]
    return grid


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    return None


def bfs(grid):
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


grid = parse(sys.argv[1])
dist = bfs(grid)
if dist is None:
    raise SystemExit("error: unsolvable")
print(f"path_length={dist}")
```

Notes: Works on a hand-made maze. Wants `gen` subcommand.

## Step 2: Add generator (guaranteed solvable path)

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


def parse(path: str):
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
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
    if width < 3 or height < 3:
        raise SystemExit("error: width/height must be >= 3")
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
        options = []
        if x < ex:
            options.append((x + 1, y))
        if y < ey:
            options.append((x, y + 1))
        if options and rng.random() < 0.8:
            x, y = rng.choice(options)
        else:
            x, y = rng.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
            x = max(1, min(width - 2, x))
            y = max(1, min(height - 2, y))
        path.add((x, y))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.28:
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
        grid = gen(args.width, args.height, args.seed)
        print_grid(grid)
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

Notes: Generates solvable mazes because the carved path is never walled.

## Step 3: Validation for characters + exactly one S/E

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

    s_count = sum(ch == "S" for row in grid for ch in row)
    e_count = sum(ch == "E" for row in grid for ch in row)
    if s_count != 1 or e_count != 1:
        raise SystemExit("error: maze must contain exactly one S and one E")
    return grid


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    raise AssertionError("unreachable")


def solve_length(grid):
    start = find(grid, "S")
    end = find(grid, "E")
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
    if width < 3 or height < 3:
        raise SystemExit("error: width/height must be >= 3")
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
        options = []
        if x < ex:
            options.append((x + 1, y))
        if y < ey:
            options.append((x, y + 1))
        if options and rng.random() < 0.8:
            x, y = rng.choice(options)
        else:
            x, y = rng.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
            x = max(1, min(width - 2, x))
            y = max(1, min(height - 2, y))
        path.add((x, y))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.28:
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
        grid = gen(args.width, args.height, args.seed)
        print_grid(grid)
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
