# Trace 01 – Planner (SVG Logo Generator)

## Plan
- Define output requirements: valid `<svg>`, contains `<text>` with the phrase.
- Add width/height flags and validation.
- Add a deterministic default theme; optional additional themes behind a flag.

## Step 1: Renderer function

Snapshot: logo.py
```python
from html import escape


def render(text: str, width: int, height: int, bg: str, fg: str) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{y}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )
```

## Step 2: CLI + default theme

Snapshot: logo.py
```python
import argparse
from html import escape


def render(text: str, width: int, height: int, bg: str, fg: str) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{y}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=["default"], default="default")
    args = p.parse_args()
    print(render(args.text, args.width, args.height, bg="#111111", fg="#ffffff"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Validation + extra theme

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#111111", "fg": "#ffffff"},
    "invert": {"bg": "#ffffff", "fg": "#111111"},
}


def render(text: str, width: int, height: int, bg: str, fg: str) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{y}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=sorted(THEMES.keys()), default="default")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    theme = THEMES[args.theme]
    print(render(args.text, args.width, args.height, bg=theme["bg"], fg=theme["fg"]), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
