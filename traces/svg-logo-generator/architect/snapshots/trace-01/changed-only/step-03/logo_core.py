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
