# Trace 01 – Improviser (ASCII Art Poster)

Starts by spiking a “cute output”, then backfills flags and validation after friction shows up.

## Step 1: Spike a poster (hard-coded width)

Snapshot: poster.py
```python
import sys

msg = " ".join(sys.argv[1:]) or "hi"
width = 24

print("+" + "-" * (width + 2) + "+")
print("| " + msg[:width].ljust(width) + " |")
print("+" + "-" * (width + 2) + "+")
```

Notes: Looks fine for short text; immediately wants wrapping.

## Step 2: Adds wrapping and alignment (forgets border=none)

Snapshot: poster.py
```python
import sys
import textwrap

msg = " ".join(sys.argv[1:]) or "hi"
width = 24
align = "center"

lines = textwrap.wrap(msg, width=width) or [""]
if align == "center":
    lines = [line.center(width) for line in lines]

print("+" + "-" * (width + 2) + "+")
for line in lines:
    print("| " + line + " |")
print("+" + "-" * (width + 2) + "+")
```

Notes: Realizes it’s time to stop abusing `sys.argv`.

## Step 3: Argparse + `--border none` + input validation

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
    mid = "".join("| " + line + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + mid + bot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=24)
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
