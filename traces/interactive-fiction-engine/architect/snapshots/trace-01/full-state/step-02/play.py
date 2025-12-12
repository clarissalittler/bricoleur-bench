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
