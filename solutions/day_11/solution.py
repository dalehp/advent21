from typing import TextIO

from solutions.common import IntGrid, Point

FILE = "solutions/day_11/input.txt"
TEST_FILE = "solutions/day_11/test_input.txt"

DIRECTIONS = (
    Point(0, 1),
    Point(1, 1),
    Point(1, 0),
    Point(1, -1),
    Point(0, -1),
    Point(-1, -1),
    Point(-1, 0),
    Point(-1, 1),
)
FLASH = 10


def increase_energy_levels(grid: IntGrid):
    for point, energy in grid:
        grid[point] = energy + 1


def process_flash(grid: IntGrid, point: Point):
    for p in (d + point for d in DIRECTIONS):
        energy = grid.get(p)
        if energy is None or energy == FLASH or energy == 0:
            continue
        grid[p] = energy + 1
    grid[point] = 0


def process_flashes(grid: IntGrid) -> int:
    to_flash = []
    for point, energy in grid:
        if energy == FLASH:
            to_flash.append(point)
    if not to_flash:
        return 0
    for p in to_flash:
        process_flash(grid, p)
    return len(to_flash)


def step(grid: IntGrid) -> int:
    flashes = 0
    increase_energy_levels(grid)
    while flashed := process_flashes(grid):
        flashes += flashed
    return flashes


def all_flash(grid: IntGrid) -> bool:
    flashes = step(grid)
    if flashes == len(grid):
        return True
    return False


def solve_part_a() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)

    flashes = 0
    for _ in range(100):
        flashes += step(grid)

    return flashes


def solve_part_b() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)

    step = 1
    while not all_flash(grid):
        step += 1

    return step


def run():
    print(solve_part_a())
    print(solve_part_b())
