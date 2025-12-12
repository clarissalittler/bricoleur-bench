# Trace 01 – Improviser (Interactive Fiction Engine)

Spikes a “working loop”, then reorganizes around friction (conditionals and end states).

## Step 1: Quick loop (no state)

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
    "ending_wave": { "text": "The figure smiles. Somehow, you feel less alone.", "end": true, "choices": [] },
    "ending_step": { "text": "You step away. The room seems quieter than before.", "end": true, "choices": [] },
    "ending_down": { "text": "You go downstairs into the unknown.", "end": true, "choices": [] }
  }
}
```

Snapshot: play.py
```python
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
```

Notes: Crashes on bad input; also wants conditional choices.

## Step 2: Adds flags and conditional choice filtering

Snapshot: play.py
```python
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
```

Notes: Still crashes on invalid inputs; time to add guardrails.

## Step 3: Argparse + input validation

Snapshot: play.py
```python
import argparse
import json


def load_story(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_choices(choices: list[dict], flags: set[str]) -> list[dict]:
    out = []
    for c in choices:
        req = c.get("requires", [])
        if all(r in flags for r in req):
            out.append(c)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(prog="play.py")
    parser.add_argument("story")
    args = parser.parse_args()

    story = load_story(args.story)
    nodes = story["nodes"]
    cur = story["start"]
    flags: set[str] = set()

    while True:
        n = nodes[cur]
        for f in n.get("sets", []):
            flags.add(f)

        print(n["text"])

        choices = filter_choices(n.get("choices", []), flags)
        if n.get("end") or not choices:
            return 0

        for i, c in enumerate(choices, start=1):
            print(f"{i}. {c['label']}")

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

        cur = choices[idx - 1]["to"]
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
