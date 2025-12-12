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
