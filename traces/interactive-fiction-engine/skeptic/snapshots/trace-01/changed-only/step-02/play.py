import json
import sys

story = json.load(open(sys.argv[1]))
nodes = story["nodes"]
cur = story["start"]

node = nodes[cur]
print(node["text"])
choices = node.get("choices", [])
for i, ch in enumerate(choices, start=1):
    print(f"{i}. {ch['label']}")
input("> ")
raise SystemExit(0)
