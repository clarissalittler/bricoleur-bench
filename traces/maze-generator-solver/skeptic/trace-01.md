# Trace 01 – Skeptic (Maze Generator + Solver)

Pins properties (S/E present, rectangular, solvable) rather than exact mazes.

## Step 1: Harness first (generated maze must be solvable)

Snapshot: harness.py
```python
import subprocess
import sys
import tempfile

gen = subprocess.run([sys.executable, "maze.py", "gen", "--width", "9", "--height", "7", "--seed", "1"], text=True, capture_output=True)
assert gen.returncode == 0
maze_text = gen.stdout
assert "S" in maze_text and "E" in maze_text

tmp = tempfile.NamedTemporaryFile("w+", delete=False)
tmp.write(maze_text)
tmp.flush()

sol = subprocess.run([sys.executable, "maze.py", "solve", tmp.name], text=True, capture_output=True)
assert sol.returncode == 0
assert sol.stdout.strip().startswith("path_length=")
```

Notes: Fails because `maze.py` doesn’t exist.

## Step 2: Minimal CLI with solvable generator and solver

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


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

Notes: Harness passes; adds strict parsing/validation next.

## Step 3: Strict validation of maze files

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
    if sum(ch == "S" for row in grid for ch in row) != 1:
        raise SystemExit("error: maze must contain exactly one S")
    if sum(ch == "E" for row in grid for ch in row) != 1:
        raise SystemExit("error: maze must contain exactly one E")
    return grid


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
