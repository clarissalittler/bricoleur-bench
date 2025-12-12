import random
import sys

words = [w.strip() for w in open(sys.argv[1]).read().splitlines() if w.strip()]
for _ in range(3):
    print(random.choice(words))
