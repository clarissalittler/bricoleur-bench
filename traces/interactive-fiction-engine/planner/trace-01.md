# Trace 01 – Planner (Interactive Fiction Engine)

## Plan
- Define story schema assumptions and a loader.
- Implement a pure “available choices” function (flags + requires).
- Build the main loop with clear exit behavior.
- Add robust input handling.

## Step 1: Loader + schema checkpoints

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
from typing import Any


def load_story(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        story = json.load(f)
    if "start" not in story or "nodes" not in story:
        raise ValueError("invalid story: missing start/nodes")
    return story
```

Notes: Keeps loader strict; errors should be clear.

## Step 2: Choice filtering (pure helper)

Snapshot: play.py
```python
import json
from typing import Any


def load_story(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        story = json.load(f)
    if "start" not in story or "nodes" not in story:
        raise ValueError("invalid story: missing start/nodes")
    return story


def available_choices(choices: list[dict[str, Any]], flags: set[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for ch in choices:
        req = ch.get("requires", [])
        if all(r in flags for r in req):
            out.append(ch)
    return out
```

Notes: Now can implement the loop without mixing the conditional logic into I/O.

## Step 3: Main loop + validation of user input

Snapshot: play.py
```python
import argparse
import json
from typing import Any


def load_story(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        story = json.load(f)
    if "start" not in story or "nodes" not in story:
        raise ValueError("invalid story: missing start/nodes")
    return story


def available_choices(choices: list[dict[str, Any]], flags: set[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
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
    nodes: dict[str, Any] = story["nodes"]
    current: str = story["start"]
    flags: set[str] = set()

    while True:
        node: dict[str, Any] = nodes[current]
        for f in node.get("sets", []):
            flags.add(f)

        print(node.get("text", ""))
        choices = available_choices(node.get("choices", []), flags)
        if node.get("end") or not choices:
            return 0

        for i, ch in enumerate(choices, start=1):
            print(f"{i}. {ch['label']}")

        raw = input("> ").strip()
        try:
            idx = int(raw)
        except ValueError:
            print("Please enter a number.\n")
            continue
        if idx < 1 or idx > len(choices):
            print("Invalid choice.\n")
            continue

        current = choices[idx - 1]["to"]
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
