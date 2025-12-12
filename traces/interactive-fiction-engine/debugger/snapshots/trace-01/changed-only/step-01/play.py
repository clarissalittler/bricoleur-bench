import json
import sys

story = json.load(open(sys.argv[1]))
nodes = story["nodes"]
cur = story["start"]

while True:
    node = nodes[cur]
    print(node["text"])
    if node.get("end"):
        break
    for i, ch in enumerate(node.get("choices", []), start=1):
        print(f"{i}. {ch['label']}")
    cur = node["choices"][int(input("> ")) - 1]["to"]
    print()
