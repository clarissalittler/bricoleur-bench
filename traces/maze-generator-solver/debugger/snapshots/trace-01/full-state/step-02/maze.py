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
