import argparse
import sys
from pathlib import Path


def format_line(todo_id: int, done: bool, title: str) -> str:
    return f"{todo_id}|{1 if done else 0}|{title}\n"


def load_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text().splitlines(True)


def save_lines(path: Path, lines: list[str]) -> None:
    path.write_text("".join(lines))


def parse_todo_id(raw_line: str) -> int:
    todo_id_str, _rest = raw_line.split("|", 1)
    return int(todo_id_str)


def next_id(lines: list[str]) -> int:
    ids = [parse_todo_id(l.rstrip("\n")) for l in lines if l.strip()]
    return max(ids, default=0) + 1


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=Path, default=Path("todos.txt"))
sub = parser.add_subparsers(dest="cmd", required=True)
add = sub.add_parser("add")
add.add_argument("title")
sub.add_parser("list")
done = sub.add_parser("done")
done.add_argument("id", type=int)
args = parser.parse_args()

lines = load_lines(args.file)

if args.cmd == "add":
    lines.append(format_line(next_id(lines), False, args.title))
    save_lines(args.file, lines)
    print("ok")
elif args.cmd == "list":
    print("".join(lines), end="")
else:
    print("no such todo", file=sys.stderr)
    raise SystemExit(1)
