import json
import sys

story = json.load(open(sys.argv[1]))
nodes = story["nodes"]
cur = story["start"]
flags: set[str] = set()

while True:
    node = nodes[cur]
    flags.update(node.get("sets", []))

    print(node["text"])
    if node.get("end"):
        break

    raw = node.get("choices", [])
    choices = []
    for ch in raw:
        req = ch.get("requires", [])
        print("debug requires=", req, "flags=", sorted(flags))
        if all(r in flags for r in req):
            choices.append(ch)

    for i, ch in enumerate(choices, start=1):
        print(f"{i}. {ch['label']}")

    cur = choices[int(input("> ")) - 1]["to"]
    print()
