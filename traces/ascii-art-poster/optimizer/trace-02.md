# Trace 02 – Optimizer (ascii-art-poster)

## Step 1: Add theme without changing default

Snapshot: poster.py
```python
import argparse
import textwrap


THEMES = {
    "default": {"corner": "+", "h": "-", "v": "|"},
    "bubble": {"corner": "o", "h": "-", "v": "|"},
}


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str, theme: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"

    t = THEMES[theme]
    top = t["corner"] + t["h"] * (width + 2) + t["corner"] + "\n"
    body = "".join(t["v"] + " " + line + " " + t["v"] + "\n" for line in lines)
    bot = top
    return top + body + bot


def main() -> int:
    p = argparse.ArgumentParser(prog="poster.py")
    p.add_argument("message")
    p.add_argument("--width", type=int, default=20)
    p.add_argument("--align", choices=["left", "center", "right"], default="left")
    p.add_argument("--border", choices=["ascii", "none"], default="ascii")
    p.add_argument("--theme", choices=sorted(THEMES.keys()), default="default")
    args = p.parse_args()

    if args.width < 1:
        raise SystemExit("error: --width must be >= 1")
    print(render(args.message, args.width, args.align, args.border, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Make default theme explicit for tests

Snapshot: poster.py
```python
import argparse
import textwrap


THEMES = {
    "default": {"corner": "+", "h": "-", "v": "|"},
    "bubble": {"corner": "o", "h": "-", "v": "|"},
}


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    return line.center(width)


def render(message: str, width: int, align: str, border: str, theme: str) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"

    t = THEMES[theme]
    top = t["corner"] + t["h"] * (width + 2) + t["corner"] + "\n"
    body = "".join(t["v"] + " " + line + " " + t["v"] + "\n" for line in lines)
    return top + body + top


def main() -> int:
    p = argparse.ArgumentParser(
        prog="poster.py",
        description="ASCII poster. Default theme is deterministic.",
    )
    p.add_argument("message")
    p.add_argument("--width", type=int, default=20)
    p.add_argument("--align", choices=["left", "center", "right"], default="left")
    p.add_argument("--border", choices=["ascii", "none"], default="ascii")
    p.add_argument("--theme", choices=sorted(THEMES.keys()), default="default")
    args = p.parse_args()

    if args.width < 1:
        raise SystemExit("error: --width must be >= 1")
    print(render(args.message, args.width, args.align, args.border, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
