# Trace 01 – Skeptic (Interactive Fiction Engine)

Pins a minimal “golden transcript” using subprocess + stdin.

## Step 1: Harness first (expects a prompt and at least one choice)

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

Snapshot: harness.py
```python
import subprocess
import sys

run = subprocess.run(
    [sys.executable, "play.py", "example-story.json"],
    input="1\n",
    text=True,
    capture_output=True,
)
assert run.returncode == 0
assert "1." in run.stdout
assert "> " in run.stdout or run.stdout.endswith("> ") or run.stdout.endswith(">\n")
```

Notes: Fails because `play.py` doesn’t exist yet.

## Step 2: Minimal `play.py` to satisfy harness shape

Snapshot: play.py
```python
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
```

Notes: Harness now passes the “shape” check; next, add correctness around conditional choices.

## Step 3: Full loop + flags + validation

Snapshot: play.py
```python
import argparse
import json


def load_story(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def available_choices(choices: list[dict], flags: set[str]) -> list[dict]:
    out = []
    for ch in choices:
        req = ch.get("requires", [])
        if all(r in flags for r in req):
            out.append(ch)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("story")
    args = parser.parse_args()

    story = load_story(args.story)
    nodes = story["nodes"]
    cur = story["start"]
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get("sets", []))
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

        cur = choices[idx - 1]["to"]
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
