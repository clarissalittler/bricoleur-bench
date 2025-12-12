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
