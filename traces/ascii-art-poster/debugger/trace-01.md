# Trace 01 – Debugger (ASCII Art Poster)

Starts from a known-bad output and adds small probes to isolate width/alignment bugs.

## Step 1: Repro case (center alignment looks off)

Snapshot: poster.py
```python
import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    lines = [line.center(width) for line in lines]
    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


print(render("one two three", 10), end="")
```

Notes: Sometimes sees uneven spacing; wants to check lengths explicitly.

## Step 2: Adds probes (length assertions)

Snapshot: poster.py
```python
import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    aligned = [line.center(width) for line in lines]
    for a in aligned:
        if len(a) != width:
            raise SystemExit(f"debug: bad width {len(a)} for {a!r}")

    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in aligned)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


print(render("one two three", 10), end="")
```

Notes: Real bug was elsewhere: `width` was being interpreted as total width sometimes. Makes it explicit in final CLI.

## Step 3: CLI with explicit semantics + border none

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
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=20, help="Inner text width (excluding border/padding)")
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
