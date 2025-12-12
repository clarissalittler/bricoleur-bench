# Trace 01 – Architect (Interactive Fiction Engine)

Front-loads a small internal model to keep parsing and gameplay separate.

## Step 1: Data model + loader module

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

Snapshot: story.py
```python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Choice:
    label: str
    to: str
    requires: tuple[str, ...] = ()


@dataclass(frozen=True)
class Node:
    text: str
    choices: tuple[Choice, ...]
    sets: tuple[str, ...] = ()
    end: bool = False


@dataclass(frozen=True)
class Story:
    start: str
    nodes: dict[str, Node]


def load_story(path: Path) -> Story:
    raw = json.loads(path.read_text(encoding="utf-8"))
    start = raw["start"]
    nodes: dict[str, Node] = {}
    for node_id, node_raw in raw["nodes"].items():
        choices = tuple(
            Choice(
                label=c["label"],
                to=c["to"],
                requires=tuple(c.get("requires", [])),
            )
            for c in node_raw.get("choices", [])
        )
        nodes[node_id] = Node(
            text=node_raw.get("text", ""),
            choices=choices,
            sets=tuple(node_raw.get("sets", [])),
            end=bool(node_raw.get("end", False)),
        )
    return Story(start=start, nodes=nodes)
```

## Step 2: Engine loop (pure-ish) and CLI

Snapshot: play.py
```python
import argparse
from pathlib import Path

from story import Story, load_story


def available_choices(story: Story, node_id: str, flags: set[str]):
    node = story.nodes[node_id]
    return [c for c in node.choices if all(r in flags for r in c.requires)]


def main() -> int:
    parser = argparse.ArgumentParser(prog="play.py")
    parser.add_argument("story", type=Path)
    args = parser.parse_args()

    story = load_story(args.story)
    cur = story.start
    flags: set[str] = set()

    while True:
        node = story.nodes[cur]
        flags.update(node.sets)
        print(node.text)

        choices = available_choices(story, cur, flags)
        if node.end or not choices:
            return 0

        for i, ch in enumerate(choices, start=1):
            print(f"{i}. {ch.label}")

        raw = input("> ").strip()
        idx = int(raw)
        cur = choices[idx - 1].to
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Input validation stays in CLI layer

Snapshot: play.py
```python
import argparse
from pathlib import Path

from story import Story, load_story


def available_choices(story: Story, node_id: str, flags: set[str]):
    node = story.nodes[node_id]
    return [c for c in node.choices if all(r in flags for r in c.requires)]


def main() -> int:
    parser = argparse.ArgumentParser(prog="play.py")
    parser.add_argument("story", type=Path)
    args = parser.parse_args()

    story = load_story(args.story)
    cur = story.start
    flags: set[str] = set()

    while True:
        node = story.nodes[cur]
        flags.update(node.sets)
        print(node.text)

        choices = available_choices(story, cur, flags)
        if node.end or not choices:
            return 0

        for i, ch in enumerate(choices, start=1):
            print(f"{i}. {ch.label}")

        raw = input("> ").strip()
        try:
            idx = int(raw)
        except ValueError:
            print("Please enter a number.\n")
            continue
        if idx < 1 or idx > len(choices):
            print("Invalid choice.\n")
            continue

        cur = choices[idx - 1].to
        print()


if __name__ == "__main__":
    raise SystemExit(main())
```
