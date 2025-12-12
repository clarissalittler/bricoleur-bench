from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Grid:
    cells: list[list[bool]]

    @property
    def height(self) -> int:
        return len(self.cells)

    @property
    def width(self) -> int:
        return len(self.cells[0]) if self.cells else 0


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def step(grid: Grid) -> Grid:
    h = grid.height
    w = grid.width
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and grid.cells[ny][nx]:
                    n += 1
            alive = grid.cells[y][x]
            out[y][x] = (alive and n in (2, 3)) or ((not alive) and n == 3)
    return Grid(out)
