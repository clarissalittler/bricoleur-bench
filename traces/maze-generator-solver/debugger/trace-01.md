# Trace 01 – Debugger (Maze Generator + Solver)

Starts from a failing generated maze (“solver says unsolvable”) and diagnoses why.

## Step 1: Generator that sometimes blocks the only corridor

Snapshot: maze.py
```python
import random
import sys

w, h, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)

grid = [["."] * w for _ in range(h)]
for y in range(h):
    for x in range(w):
        if rng.random() < 0.35:
            grid[y][x] = "#"
grid[1][1] = "S"
grid[h - 2][w - 2] = "E"

for row in grid:
    print("".join(row))
```

Notes: No solver yet, but eyeballing shows S/E can be boxed in.

## Step 2: Add solver + debug probe (count reachable cells)

Snapshot: maze.py
```python
import argparse
import random
import sys
from collections import deque


def gen(w: int, h: int, seed: int):
    rng = random.Random(seed)
    grid = [["."] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if rng.random() < 0.35:
                grid[y][x] = "#"
    grid[1][1] = "S"
    grid[h - 2][w - 2] = "E"
    return grid


def solve_length(grid):
    w = len(grid[0])
    h = len(grid)
    start = (1, 1)
    end = (w - 2, h - 2)
    q = deque([(start[0], start[1], 0)])
    seen = {start}
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d, len(seen)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                if grid[ny][nx] in (".", "E"):
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1))
    return None, len(seen)


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("--debug", action="store_true")
    s.add_argument("maze")
    args = p.parse_args()

    if args.cmd == "gen":
        grid = gen(args.width, args.height, args.seed)
        for row in grid:
            print("".join(row))
        return 0

    grid = [list(l.rstrip("\n")) for l in open(args.maze).read().splitlines() if l.strip()]
    dist, reached = solve_length(grid)
    if args.debug:
        print(f"debug reached={reached}", file=sys.stderr)
    if dist is None:
        print("error: unsolvable", file=sys.stderr)
        return 1
    print(f"path_length={dist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Debug shows tiny reachable region; fix generator by carving a guaranteed path.

## Step 3: Generator guarantees connectivity via carved path

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


def solve_length(grid):
    w = len(grid[0])
    h = len(grid)
    start = next((x, y) for y in range(h) for x in range(w) if grid[y][x] == "S")
    end = next((x, y) for y in range(h) for x in range(w) if grid[y][x] == "E")
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
        for row in grid:
            print("".join(row))
        return 0

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
