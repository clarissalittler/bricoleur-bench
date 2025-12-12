# Trace 01 – Architect (ASCII Art Poster)

Starts by separating rendering/pure functions from the CLI so later themes don’t entangle argument parsing.

## Step 1: Core module (rendering contract)

Snapshot: poster_core.py
```python
import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    if align == "center":
        return line.center(width)
    raise ValueError("align must be left|center|right")


def render(message: str, width: int, align: str, border: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"
    if border != "ascii":
        raise ValueError("border must be ascii|none")

    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot
```

## Step 2: CLI wrapper

Snapshot: poster.py
```python
import argparse

from poster_core import render


def main() -> int:
    parser = argparse.ArgumentParser(prog="poster.py", description="Render an ASCII poster.")
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

## Step 3: Leave room for themes without breaking defaults

Snapshot: poster_core.py
```python
import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    if align == "center":
        return line.center(width)
    raise ValueError("align must be left|center|right")


def render(message: str, width: int, align: str, border: str, *, padding: int = 1) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"
    if border != "ascii":
        raise ValueError("border must be ascii|none")

    border_width = width + (2 * padding) + 2
    top = "+" + "-" * border_width + "+\n"
    body = "".join("| " + (" " * padding) + line + (" " * padding) + " |\n" for line in lines)
    bot = "+" + "-" * border_width + "+\n"
    return top + body + bot
```
