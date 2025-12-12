import sys

path = sys.argv[1]
text = open(path).read().strip().splitlines()
for line in text:
    print(line)
