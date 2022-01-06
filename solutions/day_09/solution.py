import math
from dataclasses import dataclass
from typing import Iterator, TextIO

from solutions.common import Point

FILE = "solutions/day_09/input.txt"
TEST_FILE = "solutions/day_09/test_input.txt"

ULDR = (Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0))


class Grid:
    def __init__(self, f: TextIO):
        self.heights: dict[Point, int] = {}
        for j, line in enumerate(f):
            for i, character in enumerate(line.rstrip()):
                self.heights[Point(i, j)] = int(character)

    def __iter__(self) -> Iterator[tuple[Point, int]]:
        for position, height in self.heights.items():
            yield position, height

    def get_adjacent_heights(self, point: Point) -> list[int]:
        return [h for p in ULDR if (h := self.heights.get(point + p)) is not None]

    def get_basin_size(self, point: Point) -> int:
        current_height = self.heights.get(point)
        if current_height is None:
            raise ValueError("Point is not in grid")
        elif current_height == 9:
            raise ValueError("Point is at max height, not in a basin")

        visited = {point}
        size = 1
        to_visit = [v for p in ULDR if (v := point + p) in self.heights]
        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
            visited.add(current)
            height = self.heights[current]
            if height == 9:
                continue
            size += 1
            to_visit.extend([n for p in ULDR if (n := current + p) in self.heights])
        return size


def solve_part_a() -> int:
    with open(FILE) as f:
        grid = Grid(f)
    risk = 0
    for point, height in grid:
        if all(height < adj_height for adj_height in grid.get_adjacent_heights(point)):
            risk += height + 1
    return risk


def solve_part_b() -> int:
    with open(FILE) as f:
        grid = Grid(f)
    low_points = []
    for point, height in grid:
        if all(height < adj_height for adj_height in grid.get_adjacent_heights(point)):
            low_points.append(point)

    basin_sizes = [grid.get_basin_size(l) for l in low_points]
    highest_3 = sorted(basin_sizes)[-3:]
    return math.prod(highest_3)


def run():
    print(solve_part_a())
    print(solve_part_b())
