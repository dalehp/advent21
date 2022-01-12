import math
from dataclasses import dataclass

from solutions.common import IntGrid, Point, ULDR, get_adjacent_values

FILE = "solutions/day_09/input.txt"
TEST_FILE = "solutions/day_09/test_input.txt"


def get_basin_size(grid: IntGrid, point: Point) -> int:
    current_height = grid.get(point)
    if current_height is None:
        raise ValueError("Point is not in grid")
    elif current_height == 9:
        raise ValueError("Point is at max height, not in a basin")

    visited = {point}
    size = 1
    to_visit = [v for p in ULDR if (v := point + p) in grid]
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)
        height = grid[current]
        if height == 9:
            continue
        size += 1
        to_visit.extend([n for p in ULDR if (n := current + p) in grid])
    return size


def solve_part_a() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)
    risk = 0
    for point, height in grid:
        if all(height < adj_height for adj_height in get_adjacent_values(grid, point)):
            risk += height + 1
    return risk


def solve_part_b() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)
    low_points = []
    for point, height in grid:
        if all(height < adj_height for adj_height in get_adjacent_values(grid, point)):
            low_points.append(point)

    basin_sizes = [get_basin_size(grid, l) for l in low_points]
    highest_3 = sorted(basin_sizes)[-3:]
    return math.prod(highest_3)


def run():
    print(solve_part_a())
    print(solve_part_b())
