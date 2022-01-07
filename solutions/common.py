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
        for position, value in self.grid.items():
            yield position, value

    def __getitem__(self, p: Point) -> int:
        return self.grid[p]

    def __setitem__(self, p: Point, v: int):
        self.grid[p] = v

    def __contains__(self, p: Point) -> bool:
        return p in self.grid

    def __len__(self) -> int:
        return len(self.grid)

    @staticmethod
    def _char(i: int) -> str:
        if i == 10:
            return "*"
        return str(i)

    def __str__(self) -> str:
        min_x = min(p.x for p in self.grid.keys())
        max_x = max(p.x for p in self.grid.keys())
        min_z = min(p.z for p in self.grid.keys())
        max_z = max(p.z for p in self.grid.keys())

        return (
            "\n".join(
                "".join(self._char(self[Point(i, j)]) for i in range(min_x, max_x + 1))
                for j in range(min_z, max_z + 1)
            )
            + "\n"
        )

    def get(self, p: Point) -> Optional[int]:
        return self.grid.get(p)
