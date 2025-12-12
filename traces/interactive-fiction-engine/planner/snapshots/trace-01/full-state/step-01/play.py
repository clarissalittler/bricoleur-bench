import json
from typing import Any


def load_story(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        story = json.load(f)
    if "start" not in story or "nodes" not in story:
        raise ValueError("invalid story: missing start/nodes")
    return story
