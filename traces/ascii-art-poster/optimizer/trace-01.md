# Trace 01 – Optimizer (ASCII Art Poster)

Builds a correct baseline, then tweaks for speed/clarity on large inputs (many wrapped lines).

## Step 1: Baseline (works, a bit allocation-heavy)

Snapshot: poster.py
```python
import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line.ljust(width) + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot
```

Notes: Plans to avoid repeated string concatenation patterns once correctness is pinned.

## Step 2: Precompute border strings; avoid generator join surprises

Snapshot: poster.py
```python
import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]

    top = "+" + "-" * (width + 2) + "+\n"
    bot = top

    out: list[str] = [top]
    for line in lines:
        out.append("| " + line.ljust(width) + " |\n")
    out.append(bot)
    return "".join(out)
```

Notes: Same output, fewer intermediate strings when there are many lines.

## Step 3: Add CLI flags (keeps default deterministic)

Snapshot: poster.py
```python
import argparse
import textwrap


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str) -> str:
    lines = textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]
    lines = [align_line(line, width, align) for line in lines]

    if border == "none":
        return "\n".join(lines) + "\n"

    top = "+" + "-" * (width + 2) + "+\n"
    out: list[str] = [top]
    for line in lines:
        out.append("| " + line + " |\n")
    out.append(top)
    return "".join(out)


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
