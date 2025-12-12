import json
import sys

story = json.load(open(sys.argv[1]))
nodes = story["nodes"]
cur = story["start"]

while True:
    n = nodes[cur]
    print(n["text"])
    if n.get("end"):
        break
    choices = n.get("choices", [])
    for i, c in enumerate(choices, start=1):
        print(i, c["label"])
    cur = choices[int(input("> ")) - 1]["to"]
    print()
