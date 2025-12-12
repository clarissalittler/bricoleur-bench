from __future__ import annotations

from dataclasses import dataclass


ALLOWED = {"#", ".", "S", "E"}


@dataclass(frozen=True)
class Maze:
    grid: list[list[str]]

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)


def parse(path: str) -> Maze:
    lines = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        raise ValueError("empty maze")
    w = len(lines[0])
    if any(len(l) != w for l in lines):
        raise ValueError("ragged maze")
    grid = [list(l) for l in lines]
    for row in grid:
        for ch in row:
            if ch not in ALLOWED:
                raise ValueError("unknown character in maze")
    if sum(ch == "S" for row in grid for ch in row) != 1:
        raise ValueError("maze must contain exactly one S")
    if sum(ch == "E" for row in grid for ch in row) != 1:
        raise ValueError("maze must contain exactly one E")
    return Maze(grid)


def render(maze: Maze) -> str:
    return "\n".join("".join(row) for row in maze.grid) + "\n"
