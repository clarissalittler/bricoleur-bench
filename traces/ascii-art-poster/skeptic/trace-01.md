# Trace 01 – Skeptic (ASCII Art Poster)

Writes a tiny “expected output” harness first so changes don’t silently drift.

## Step 1: Pin an expected default output for `"hi"`

Snapshot: harness.py
```python
import subprocess
import sys

expected = "+----+\n| hi |\n+----+\n"
out = subprocess.run([sys.executable, "poster.py", "hi", "--width", "2"], text=True, capture_output=True)
assert out.returncode == 0
assert out.stdout == expected
```

Notes: This fails because `poster.py` doesn’t exist yet.

## Step 2: Minimal `poster.py` to satisfy the harness

Snapshot: poster.py
```python
import argparse


def render(message: str, width: int) -> str:
    inside = message[:width].ljust(width)
    top = "+" + "-" * (width + 2) + "+\n"
    return top + "| " + inside + " |\n" + top


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=20)
    args = parser.parse_args()

    if args.width < 1:
        raise SystemExit(1)

    print(render(args.message, args.width), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Harness passes for the pinned case.

## Step 3: Expand to align + border none (adds new checks)

Snapshot: poster.py
```python
import argparse
import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"

    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in lines)
    return top + body + top


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=20)
    parser.add_argument("--align", choices=["left", "center", "right"], default="left")
    parser.add_argument("--border", choices=["ascii", "none"], default="ascii")
    args = parser.parse_args()

    if args.width < 1:
        raise SystemExit("error: --width must be >= 1")

    print(render(args.message, args.width, args.align, args.border), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
