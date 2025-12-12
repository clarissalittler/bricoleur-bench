import sys


def neighbor_count(lines: list[str], x: int, y: int) -> int:
    h = len(lines)
    w = len(lines[0])
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                n += 1
    return n


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = neighbor_count(lines, x, y)
            if (x, y) == (2, 2):
                print("debug center neighbors=", n)
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


lines = [l.rstrip("\n") for l in open(sys.argv[1]).read().splitlines() if l.strip()]
print("\n".join(lines))
print()
print("\n".join(step(lines)))
