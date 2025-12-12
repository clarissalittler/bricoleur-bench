import argparse


def parse_grid(path: str) -> list[list[str]]:
    lines = [line.rstrip("\n") for line in open(path).read().splitlines() if line.strip()]
    w = len(lines[0])
    if any(len(line) != w for line in lines):
        raise SystemExit("error: ragged grid")
    return [list(line) for line in lines]


def count_neighbors(grid: list[list[str]], x: int, y: int) -> int:
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            if grid[y + dy][x + dx] == "#":  # oops: crashes at edges
                n += 1
    return n


def step(grid: list[list[str]]) -> list[list[str]]:
    h = len(grid)
    w = len(grid[0])
    out = [["."] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            alive = grid[y][x] == "#"
            neighbors = count_neighbors(grid, x, y)
            if alive and neighbors in (2, 3):
                out[y][x] = "#"
            elif (not alive) and neighbors == 3:
                out[y][x] = "#"
    return out


def print_grid(grid: list[list[str]]) -> None:
    for row in grid:
        print("".join(row))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern")
    args = p.parse_args()

    grid = parse_grid(args.pattern)
    print_grid(grid)
    for _ in range(args.steps):
        print()
        grid = step(grid)
        print_grid(grid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
