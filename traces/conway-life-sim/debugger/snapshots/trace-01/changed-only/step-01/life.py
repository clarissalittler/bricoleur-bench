import sys


def step(lines: list[str]) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                        n += 1
            alive = lines[y][x] == "#"
            # bug: mistakenly keeps cells alive at n==4
            row.append("#" if (alive and n in (2, 3, 4)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


lines = [l.rstrip("\n") for l in open(sys.argv[1]).read().splitlines() if l.strip()]
print("\n".join(lines))
print()
print("\n".join(step(lines)))
