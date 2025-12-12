def parse_grid(path: str) -> list[list[str]]:
    lines = [line.rstrip("\n") for line in open(path).read().splitlines() if line.strip()]
    if not lines:
        raise SystemExit("error: empty pattern")
    w = len(lines[0])
    if any(len(line) != w for line in lines):
        raise SystemExit("error: ragged grid")
    for line in lines:
        for ch in line:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")
    return [list(line) for line in lines]


def count_neighbors(grid: list[list[str]], x: int, y: int) -> int:
    h = len(grid)
    w = len(grid[0])
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            ny = y + dy
            nx = x + dx
            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] == "#":
                n += 1
    return n


def step(grid: list[list[str]]) -> list[list[str]]:
    h = len(grid)
    w = len(grid[0])
    out = [["."] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            alive = grid[y][x] == "#"
            n = count_neighbors(grid, x, y)
            if alive and n in (2, 3):
                out[y][x] = "#"
            elif (not alive) and n == 3:
                out[y][x] = "#"
    return out
