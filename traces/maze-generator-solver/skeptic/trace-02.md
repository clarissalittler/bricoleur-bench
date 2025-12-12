# Trace 02 – Skeptic (maze-generator-solver)

## Step 1: Keep solver output stable; add optional `--show-path`

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


def solve_path(grid):
    start = find(grid, "S")
    end = find(grid, "E")
    if not start or not end:
        raise SystemExit("error: missing S or E")
    w = len(grid[0])
    h = len(grid)
    q = deque([start])
    prev = {start: None}
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in prev:
                if grid[ny][nx] in (".", "E"):
                    prev[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    if end not in prev:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def gen(width: int, height: int, seed: int):
    rng = random.Random(seed)
    grid = [["#"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = "."
    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    x, y = sx, sy
    path = {(x, y)}
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


def overlay(grid, path):
    g = [row[:] for row in grid]
    for (x, y) in path:
        if g[y][x] == ".":
            g[y][x] = "*"
    return g


def main() -> int:
    p = argparse.ArgumentParser(prog="maze.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("--show-path", action="store_true")
    s.add_argument("maze")
    args = p.parse_args()

    if args.cmd == "gen":
        print_grid(gen(args.width, args.height, args.seed))
        return 0

    grid = parse(args.maze)
    path = solve_path(grid)
    if path is None:
        print("error: unsolvable", file=sys.stderr)
        return 1
    print(f"path_length={len(path)-1}")
    if args.show_path:
        print()
        print_grid(overlay(grid, path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Keep parser strict about exactly one S/E

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


def find(grid, ch):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ch:
                return x, y
    raise AssertionError("unreachable")


def solve_path(grid):
    start = find(grid, "S")
    end = find(grid, "E")
    w = len(grid[0])
    h = len(grid)
    q = deque([start])
    prev = {start: None}
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in prev:
                if grid[ny][nx] in (".", "E"):
                    prev[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    if end not in prev:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


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
    x, y = sx, sy
    path = {(x, y)}
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


def overlay(grid, path):
    g = [row[:] for row in grid]
    for (x, y) in path:
        if g[y][x] == ".":
            g[y][x] = "*"
    return g


def main() -> int:
    p = argparse.ArgumentParser(prog="maze.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("--show-path", action="store_true")
    s.add_argument("maze")
    args = p.parse_args()

    if args.cmd == "gen":
        print_grid(gen(args.width, args.height, args.seed))
        return 0

    grid = parse(args.maze)
    path = solve_path(grid)
    if path is None:
        print("error: unsolvable", file=sys.stderr)
        return 1
    print(f"path_length={len(path)-1}")
    if args.show_path:
        print()
        print_grid(overlay(grid, path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
