# Trace 01 – Bricoleur (ASCII Art Poster)

Goal: get *something* on screen quickly, then keep nudging it until it matches the acceptance criteria.

## Step 1: Quick bordered box (no wrapping yet)

Snapshot: poster.py
```python
message = " ".join(__import__("sys").argv[1:]) or "hi"

width = 20
inside = message[:width].ljust(width)

print("+" + "-" * (width + 2) + "+")
print("| " + inside + " |")
print("+" + "-" * (width + 2) + "+")
```

Run: `python poster.py hi` prints a box; long messages get chopped (fine for now).

## Step 2: Adds wrapping; miscounts the border width once

Uses `textwrap.wrap`, but gets an off-by-two in the border line.

Snapshot: poster.py
```python
import sys
import textwrap

message = " ".join(sys.argv[1:]) or "hi"

width = 20
lines = textwrap.wrap(message, width=width) or [""]

print("+" + "-" * width + "+")  # oops: should include padding
for line in lines:
    print("| " + line.ljust(width) + " |")
print("+" + "-" * width + "+")
```

Notes: Notices the top/bottom look shorter than the body; fixes next step.

## Step 3: Proper CLI + align + border=none

Snapshot: poster.py
```python
import argparse
import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    lines = textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False)
    return lines if lines else [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    if align == "center":
        return line.center(width)
    raise ValueError(f"unknown align: {align}")


def render(message: str, width: int, align: str, border: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"
    if border != "ascii":
        raise ValueError(f"unknown border: {border}")

    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


def main() -> int:
    parser = argparse.ArgumentParser(prog="poster.py", description="Render a simple ASCII poster.")
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

Spot checks:
- `python poster.py "hi"` prints a bordered poster and exits 0.
- `python poster.py --border none "hi"` prints just `hi` and exits 0.
- `python poster.py --align center --width 10 "one two three"` wraps deterministically.
