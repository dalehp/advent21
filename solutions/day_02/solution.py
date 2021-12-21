from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator, TextIO


class Direction(Enum):
    forward = auto()
    up = auto()
    down = auto()


@dataclass
class Point:
    x: int
    z: int  # Depth (higher is deeper)

    def __add__(self, o: Point) -> Point:
        return Point(x=self.x + o.x, z=self.z + o.z)

    def __mul__(self, o: int) -> Point:
        return Point(x=o * self.x, z=o * self.z)

    def __rmul__(self, o: int) -> Point:
        return self.__mul__(o)


@dataclass
class Movement:
    direction: Direction
    length: int


DIRECTION_TO_VECTOR: dict[Direction, Point] = {
    Direction.forward: Point(1, 0),
    Direction.up: Point(0, -1),
    Direction.down: Point(0, 1),
}


def movement_to_vector(move: Movement) -> Point:
    dir_v = DIRECTION_TO_VECTOR[move.direction]
    return dir_v * move.length


def movements_from_file(f: TextIO) -> Generator[Movement, None, None]:
    for line in f:
        d, l = line.split()
        direction = Direction[d]
        length = int(l)
        yield Movement(direction, length)


def solve_part_a() -> int:
    location = Point(0, 0)
    with open("solutions/day_02/input.txt") as f:
        for m in movements_from_file(f):
            v = movement_to_vector(m)
            location += v

    return location.x * location.z


if __name__ == "__main__":
    print(solve_part_a())
