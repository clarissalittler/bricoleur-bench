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
