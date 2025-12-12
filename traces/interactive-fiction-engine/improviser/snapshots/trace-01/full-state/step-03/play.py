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
