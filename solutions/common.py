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
    def __init__(self):
        self.grid: dict[Point, int] = {}

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

    def __add__(self, o: IntGrid) -> IntGrid:
        return self.from_dict({**self.grid, **o})

    @staticmethod
    def from_dict(d: dict[Point, int]) -> IntGrid:
        grid = IntGrid()
        grid.grid = d
        return grid

    @staticmethod
    def from_file(f: TextIO) -> IntGrid:
        grid = IntGrid()
        for j, line in enumerate(f):
            for i, character in enumerate(line.rstrip()):
                grid[Point(i, j)] = int(character)
        return grid

    @staticmethod
    def _char(i: int) -> str:
        if i == 10:
            return "*"
        return str(i)

    def __str__(self) -> str:
        min_point, max_point = self.bounds
        min_x = min_point.x
        max_x = max_point.x
        min_z = min_point.z
        max_z = max_point.z

        return (
            "\n".join(
                "".join(self._char(self[Point(i, j)]) for i in range(min_x, max_x + 1))
                for j in range(min_z, max_z + 1)
            )
            + "\n"
        )

    def get(self, p: Point) -> Optional[int]:
        return self.grid.get(p)

    @property
    def bounds(self) -> tuple[Point, Point]:
        min_x = min(p.x for p in self.grid.keys())
        max_x = max(p.x for p in self.grid.keys())
        min_z = min(p.z for p in self.grid.keys())
        max_z = max(p.z for p in self.grid.keys())
        return Point(min_x, min_z), Point(max_x, max_z)

ULDR = (Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0))

def get_adjacent_values(grid: IntGrid, point: Point) -> list[int]:
    return [h for p in ULDR if (h := grid.get(point + p)) is not None]

def adjacent_points_and_values(grid: IntGrid, point: Point) -> list[tuple[Point, int]]:
    return [(point + p, h) for p in ULDR if (h := grid.get(point + p)) is not None]