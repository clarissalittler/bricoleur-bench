import json
import sys

story = json.load(open(sys.argv[1]))
nodes = story["nodes"]
cur = story["start"]
flags: set[str] = set()

while True:
    n = nodes[cur]
    for f in n.get("sets", []):
        flags.add(f)

    print(n["text"])
    if n.get("end"):
        break

    raw = n.get("choices", [])
    choices = []
    for c in raw:
        req = c.get("requires", [])
        if all(r in flags for r in req):
            choices.append(c)

    for i, c in enumerate(choices, start=1):
        print(f"{i}. {c['label']}")

    cur = choices[int(input("> ")) - 1]["to"]
    print()
