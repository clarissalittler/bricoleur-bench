# Trace 01 – Bricoleur (Interactive Fiction Engine)

Starts by printing *something*, then keeps wiring until choices work.

## Step 1: Load JSON and print the start node

Snapshot: example-story.json
```json
{
  "start": "wake",
  "nodes": {
    "wake": {
      "text": "You wake in a quiet room. There is a door and a window.",
      "choices": [
        { "label": "Open the door", "to": "hall" },
        { "label": "Look out the window", "to": "window", "requires": ["curtain_open"] },
        { "label": "Pull the curtain aside", "to": "curtain" }
      ]
    },
    "curtain": {
      "text": "Dusty light spills in. The street outside looks empty.",
      "sets": ["curtain_open"],
      "choices": [
        { "label": "Look out the window", "to": "window" },
        { "label": "Open the door", "to": "hall" }
      ]
    },
    "window": {
      "text": "You see your reflection and, behind it, someone waving from the street.",
      "choices": [
        { "label": "Wave back", "to": "ending_wave" },
        { "label": "Step away", "to": "ending_step" }
      ]
    },
    "hall": {
      "text": "The hallway smells like old books. A staircase leads down.",
      "choices": [
        { "label": "Go downstairs", "to": "ending_down" },
        { "label": "Go back", "to": "wake" }
      ]
    },
    "ending_wave": {
      "text": "The figure smiles. Somehow, you feel less alone.",
      "end": true,
      "choices": []
    },
    "ending_step": {
      "text": "You step away. The room seems quieter than before.",
      "end": true,
      "choices": []
    },
    "ending_down": {
      "text": "You go downstairs into the unknown.",
      "end": true,
      "choices": []
    }
  }
}
```

Snapshot: play.py
```python
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "example-story.json"
story = json.load(open(path))

start = story["start"]
node = story["nodes"][start]
print(node["text"])
```

Notes: Good enough to see the story loads; now wants choices.

## Step 2: Add choices and a simple input loop (index bug)

Snapshot: play.py
```python
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
```

Notes: Realizes humans expect choices starting at 1; fixes and adds guards.

## Step 3: State flags + conditional choices + robust input

Snapshot: play.py
```python
import argparse
import json


def load_story(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def available_choices(choices: list[dict], flags: set[str]) -> list[dict]:
    out: list[dict] = []
    for ch in choices:
        req = ch.get("requires", [])
        if all(r in flags for r in req):
            out.append(ch)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(prog="play.py")
    parser.add_argument("story")
    args = parser.parse_args()

    story = load_story(args.story)
    nodes = story["nodes"]
    current = story["start"]
    flags: set[str] = set()

    while True:
        node = nodes[current]
        for flag in node.get("sets", []):
            flags.add(flag)

        print(node["text"])

        raw_choices = node.get("choices", [])
        choices = available_choices(raw_choices, flags)
        if node.get("end") or not choices:
            return 0

        for i, ch in enumerate(choices, start=1):
            print(f"{i}. {ch['label']}")

        raw = input("> ").strip()
        try:
            idx = int(raw)
        except ValueError:
            print("Please enter a number.")
            print()
            continue

        if idx < 1 or idx > len(choices):
            print("Invalid choice.")
            print()
            continue

        current = choices[idx - 1]["to"]
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
