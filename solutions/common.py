from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional, TextIO


@dataclass(frozen=True)
class Point:
    x: int = 0
    z: int = 0  # Depth (higher is deeper)

    def __add__(self, o: Point) -> Point:
        return Point(x=self.x + o.x, z=self.z + o.z)

    def __mul__(self, o: int) -> Point:
        return Point(x=o * self.x, z=o * self.z)

    def __rmul__(self, o: int) -> Point:
        return self.__mul__(o)


class IntGrid:
    def __init__(self, f: TextIO):
        self.grid: dict[Point, int] = {}
        for j, line in enumerate(f):
            for i, character in enumerate(line.rstrip()):
                self.grid[Point(i, j)] = int(character)

    def __iter__(self) -> Iterator[tuple[Point, int]]:
        for position, height in self.grid.items():
            yield position, height

    def __getitem__(self, p: Point) -> int:
        return self.grid[p]

    def __contains__(self, p: Point) -> bool:
        return p in self.grid

    def get(self, p: Point) -> Optional[int]:
        return self.grid.get(p)
