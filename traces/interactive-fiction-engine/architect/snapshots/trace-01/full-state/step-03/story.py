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
