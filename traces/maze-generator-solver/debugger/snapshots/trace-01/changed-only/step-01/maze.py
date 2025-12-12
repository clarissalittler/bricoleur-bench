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
