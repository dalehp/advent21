from dataclasses import dataclass
from enum import Enum, auto
from typing import TextIO

from solutions.common import Point

FILE = "solutions/day_13/input.txt"
TEST_FILE = "solutions/day_13/test_input.txt"


class Axis(Enum):
    X = auto()
    Y = auto()


Grid = set[Point]


@dataclass
class Fold:
    axis: Axis
    position: int


def get_grid_and_folds_from_file(f: TextIO) -> tuple[Grid, list[Fold]]:
    grid = set()
    while l := f.readline().rstrip():
        x, y = l.split(",")
        grid.add(Point(int(x), int(y)))
    folds = []
    for l in f:
        axis_str, position = l.rstrip().split("=")
        _, axis = axis_str.split("fold along ")
        folds.append(Fold(axis=Axis[axis.upper()], position=int(position)))
    return grid, folds


def fold_point(point: Point, fold: Fold) -> Point:
    if fold.axis is Axis.X:
        if point.x < fold.position:
            return point
        return point + Point(2 * (fold.position - point.x), 0)
    elif fold.axis is Axis.Y:
        if point.z < fold.position:
            return point
        return point + Point(0, 2 * (fold.position - point.z))
    raise ValueError(f"Unexpected axis {fold.axis}")


def fold_grid(grid: Grid, fold: Fold) -> Grid:
    new_grid = set()
    for point in grid:
        new_grid.add(fold_point(point, fold))
    return new_grid


def grid_to_str(grid: Grid) -> str:
    min_x = min(p.x for p in grid)
    max_x = max(p.x for p in grid)
    min_z = min(p.z for p in grid)
    max_z = max(p.z for p in grid)

    return (
        "\n".join(
            "".join(
                "*" if Point(i, j) in grid else "." for i in range(min_x, max_x + 1)
            )
            for j in range(min_z, max_z + 1)
        )
        + "\n"
    )


def solve_part_a() -> int:
    with open(FILE) as f:
        grid, folds = get_grid_and_folds_from_file(f)
    grid = fold_grid(grid, folds[0])
    return len(grid)


def solve_part_b() -> int:
    with open(FILE) as f:
        grid, folds = get_grid_and_folds_from_file(f)
    for fold in folds:
        grid = fold_grid(grid, fold)
    print(grid_to_str(grid))

    # Answer is printed to screen
    return 0


def run():
    print(solve_part_a())
    print(solve_part_b())
