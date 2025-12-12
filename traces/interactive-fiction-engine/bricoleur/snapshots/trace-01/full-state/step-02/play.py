import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "example-story.json"
story = json.load(open(path))

current = story["start"]
nodes = story["nodes"]

while True:
    node = nodes[current]
    print(node["text"])

    choices = node.get("choices", [])
    if node.get("end") or not choices:
        break

    for i, ch in enumerate(choices):
        print(f"{i}. {ch['label']}")  # 0-based… whoops

    raw = input("> ").strip()
    idx = int(raw)
    current = choices[idx]["to"]
    print()
