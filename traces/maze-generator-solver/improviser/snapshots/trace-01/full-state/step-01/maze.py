import random
import sys

w, h, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)

for y in range(h):
    row = []
    for x in range(w):
        row.append("." if rng.random() < 0.7 else "#")
    print("".join(row))
