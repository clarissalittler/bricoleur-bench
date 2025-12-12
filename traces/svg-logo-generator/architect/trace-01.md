# Trace 01 – Architect (SVG Logo Generator)

Separates “layout + theme” (pure) from CLI to keep future shapes/themes clean.

## Step 1: Theme + rendering module

Snapshot: logo_core.py
```python
from __future__ import annotations

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Theme:
    bg: str
    fg: str


THEMES = {
    "default": Theme(bg="#111111", fg="#ffffff"),
    "invert": Theme(bg="#ffffff", fg="#111111"),
}


def render_svg(text: str, width: int, height: int, theme: Theme) -> str:
    t = escape(text)
    y = height // 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{theme.bg}"/>',
        f'<text x="20" y="{y}" fill="{theme.fg}" font-size="32">{t}</text>',
        "</svg>",
        "",
    ]
    return "\n".join(parts)
```

## Step 2: CLI wrapper with validation

Snapshot: logo.py
```python
import argparse
import sys

from logo_core import THEMES, render_svg


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
    print(render_svg(args.text, args.width, args.height, theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 3: Add room for layout changes without affecting defaults

Snapshot: logo_core.py
```python
from __future__ import annotations

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Theme:
    bg: str
    fg: str


THEMES = {
    "default": Theme(bg="#111111", fg="#ffffff"),
    "invert": Theme(bg="#ffffff", fg="#111111"),
}


def render_svg(text: str, width: int, height: int, theme: Theme, *, padding: int = 20) -> str:
    t = escape(text)
    y = height // 2
    x = padding
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{theme.bg}"/>',
        f'<text x="{x}" y="{y}" fill="{theme.fg}" font-size="32">{t}</text>',
        "</svg>",
        "",
    ]
    return "\n".join(parts)
```
