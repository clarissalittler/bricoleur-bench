import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "example-story.json"
story = json.load(open(path))

start = story["start"]
node = story["nodes"][start]
print(node["text"])
