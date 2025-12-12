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
