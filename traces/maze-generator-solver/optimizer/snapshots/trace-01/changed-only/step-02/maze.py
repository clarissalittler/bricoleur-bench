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
