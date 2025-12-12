import argparse
import json


def load_story(path: str) -> tuple[str, dict[str, dict]]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    start = raw["start"]
    nodes = raw["nodes"]
    return start, nodes


def filter_choices(choices: list[dict], flags: set[str]) -> list[dict]:
    out = []
    for c in choices:
        req = c.get("requires", [])
        if all(r in flags for r in req):
            out.append(c)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("story")
    args = parser.parse_args()

    cur, nodes = load_story(args.story)
    flags: set[str] = set()

    while True:
        node = nodes[cur]
        flags.update(node.get("sets", []))
        print(node.get("text", ""))

        choices = filter_choices(node.get("choices", []), flags)
        if node.get("end") or not choices:
            return 0

        for i, ch in enumerate(choices, start=1):
            print(f"{i}. {ch['label']}")

        raw = input("> ").strip()
        idx = int(raw)
        cur = choices[idx - 1]["to"]
        print()


if __name__ == "__main__":
    raise SystemExit(main())
