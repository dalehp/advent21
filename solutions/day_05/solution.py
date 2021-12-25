import copy
import itertools
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from os import pipe
from typing import Iterator, TextIO

from solutions.common import Point

FILE = "solutions/day_05/input.txt"
TEST_FILE = "solutions/day_05/test_input.txt"


@dataclass
class Pipe:
    start: Point
    end: Point

    def points(self, include_diagonal: bool = False) -> Iterator[Point]:
        position = copy.copy(self.start)

        horiz_distance = self.end.x - self.start.x
        # Special case for vertical pipes
        if horiz_distance == 0:
            yield from self._vertical_points(position)
            return

        slope = Fraction(
            numerator=self.end.z - self.start.z, denominator=self.end.x - self.start.x
        )
        if slope != 0 and not include_diagonal:
            return

        x_direction = 1 if horiz_distance > 0 else -1
        increment = Point(
            x=x_direction * slope.denominator,
            z=x_direction * slope.denominator * slope.numerator,
        )

        yield position
        while position.x != self.end.x:
            position += increment
            yield position

    def _vertical_points(self, position: Point) -> Iterator[Point]:
        vertical_distance = self.end.z - self.start.z
        z_direction = 1 if vertical_distance > 0 else -1

        increment = Point(0, z_direction)

        yield position
        while position.z != self.end.z:
            position += increment
            yield position


def yield_pipes_from_file(f: TextIO) -> Iterator[Pipe]:
    for line in f:
        start_str, _, end_str = line.split()
        sx, sy = tuple(int(x) for x in start_str.split(","))
        ex, ey = tuple(int(x) for x in end_str.split(","))
        yield Pipe(Point(sx, sy), Point(ex, ey))


def solve_part_a(diag: bool = False) -> int:
    with open(FILE) as f:
        all_points = itertools.chain.from_iterable(
            p.points(include_diagonal=diag) for p in yield_pipes_from_file(f)
        )
        pipe_counter = Counter(all_points)

    crossing_points = 0
    for _, count in pipe_counter.most_common():
        if count == 1:
            break
        crossing_points += 1
    return crossing_points


def solve_part_b() -> int:
    return solve_part_a(diag=True)


def run():
    print(solve_part_a())
    print(solve_part_b())
