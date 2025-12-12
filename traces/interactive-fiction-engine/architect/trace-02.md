# Trace 02 – Architect (interactive-fiction-engine)

## Step 1: Add strict validation of story graph

Snapshot: play.py
```python
import argparse
import json
import sys


def load_story(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(story: dict) -> list[str]:
    errors: list[str] = []
    if "start" not in story or "nodes" not in story:
        return ["missing start/nodes"]
    nodes = story["nodes"]
    start = story["start"]
    if start not in nodes:
        errors.append(f"start node not found: {start}")
    for node_id, node in nodes.items():
        for ch in node.get("choices", []):
            to = ch.get("to")
            if to not in nodes:
                errors.append(f"{node_id}: choice target missing: {to}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(prog="play.py")
    p.add_argument("story")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    story = load_story(args.story)
    errs = validate(story)
    if errs and args.strict:
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        return 1

    nodes = story["nodes"]
    cur = story["start"]
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get("sets", []))
        print(node.get("text", ""))
        choices = []
        for c in node.get("choices", []):
            req = c.get("requires", [])
            if all(r in flags for r in req):
                choices.append(c)
        if node.get("end") or not choices:
            return 0
        for i, c in enumerate(choices, start=1):
            print(f"{i}. {c['label']}")
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

## Step 2: Provide a small second example story with a deliberate bug

Snapshot: example-story-02.json
```json
{
  "start": "start",
  "nodes": {
    "start": {
      "text": "A fork in the road.",
      "choices": [
        { "label": "Go left", "to": "left" },
        { "label": "Go right", "to": "missing_node" }
      ]
    },
    "left": { "text": "Left is quiet.", "end": true, "choices": [] }
  }
}
```

Snapshot: play.py
```python
import argparse
import json
import sys


def load_story(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(story: dict) -> list[str]:
    errors: list[str] = []
    if "start" not in story or "nodes" not in story:
        return ["missing start/nodes"]
    nodes = story["nodes"]
    start = story["start"]
    if start not in nodes:
        errors.append(f"start node not found: {start}")
    for node_id, node in nodes.items():
        for ch in node.get("choices", []):
            to = ch.get("to")
            if to not in nodes:
                errors.append(f"{node_id}: choice target missing: {to}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(prog="play.py")
    p.add_argument("story")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    story = load_story(args.story)
    errs = validate(story)
    if errs and args.strict:
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        return 1

    nodes = story["nodes"]
    cur = story["start"]
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get("sets", []))
        print(node.get("text", ""))
        choices = []
        for c in node.get("choices", []):
            req = c.get("requires", [])
            if all(r in flags for r in req):
                choices.append(c)
        if node.get("end") or not choices:
            return 0
        for i, c in enumerate(choices, start=1):
            print(f"{i}. {c['label']}")
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
        if cur not in nodes:
            print(f"error: story references missing node: {cur}", file=sys.stderr)
            return 1
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
