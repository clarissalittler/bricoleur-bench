from __future__ import annotations

from pathlib import Path

from life_core import Grid


def parse_grid(path: Path) -> Grid:
    raw = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not raw:
        raise ValueError("empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise ValueError("ragged grid")
    for l in raw:
        for ch in l:
            if ch not in (".", "#"):
                raise ValueError("grid must contain only . and #")
    return Grid([[ch == "#" for ch in l] for l in raw])


def render(grid: Grid) -> str:
    return "\n".join("".join("#" if c else "." for c in row) for row in grid.cells)
