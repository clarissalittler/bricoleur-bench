import sys

words = [w.strip() for w in open(sys.argv[1]).read().splitlines() if w.strip()]
print(words[0], words[1], words[2])
print(words[3], words[4], words[5])
print(words[6], words[7], words[8])
