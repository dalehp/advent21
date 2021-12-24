from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterator, TextIO

from solutions.common import Point


class Direction(Enum):
    forward = auto()
    up = auto()
    down = auto()


@dataclass
class Movement:
    direction: Direction
    length: int


@dataclass
class Ship:
    location: Point = field(default_factory=Point)
    aim: int = 0

    def move_ship(self, move: Movement):
        match move.direction:
            case Direction.up:
                self.aim -= move.length
            case Direction.down:
                self.aim += move.length
            case Direction.forward:
                v = Point(move.length, move.length * self.aim)
                self.location += v
            case _:
                raise ValueError


DIRECTION_TO_VECTOR: dict[Direction, Point] = {
    Direction.forward: Point(1, 0),
    Direction.up: Point(0, -1),
    Direction.down: Point(0, 1),
}


def movement_to_vector(move: Movement) -> Point:
    dir_v = DIRECTION_TO_VECTOR[move.direction]
    return dir_v * move.length


def movements_from_file(f: TextIO) -> Iterator[Movement]:
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


def solve_part_b() -> int:
    ship = Ship()
    with open("solutions/day_02/input.txt") as f:
        for m in movements_from_file(f):
            ship.move_ship(m)

    return ship.location.x * ship.location.z


def run():
    print(solve_part_a())
    print(solve_part_b())
