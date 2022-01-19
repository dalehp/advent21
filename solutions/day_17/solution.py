import re
from itertools import count
from time import sleep
from typing import TextIO

from solutions.common import Point

FILE = "solutions/day_17/input.txt"
TEST_FILE = "solutions/day_17/test_input.txt"


def get_target_ranges(f: TextIO) -> tuple[range, range]:
    input_str = f.readline().rstrip()
    res = re.match(r"target area: x=(.*)\.\.(.*), y=(.*)\.\.(.*)", input_str)
    if not res:
        raise ValueError("input format bad")
    x_range = range(int(res.group(1)), int(res.group(2)) + 1)
    y_range = range(int(res.group(3)), int(res.group(4)) + 1)
    return x_range, y_range


def step_velocity(v: Point) -> Point:
    if v.x > 0:
        x_change = -1
    elif v.x < 0:
        x_change = 1
    else:
        # v.x == 0
        x_change = 0
    return Point(v.x + x_change, v.z - 1)


def move_probe(start: Point, velocity: Point, floor: int) -> list[Point]:
    points = [start]
    while velocity.z > 0 or start.z >= floor:
        start += velocity
        points.append(start)
        velocity = step_velocity(velocity)
    return points


def attempt_map(
    points: list[Point], target_x_range: range, target_y_range: range
) -> str:
    x_points = [*(p.x for p in points), *target_x_range]
    y_points = [*(p.z for p in points), *target_y_range]
    min_x_point = min(x_points)
    min_y_point = min(y_points)
    max_x_point = max(x_points)
    max_y_point = max(y_points)

    set_points = set(points)

    pixels = []
    for j in range(max_y_point, min_y_point - 1, -1):
        for i in range(min_x_point, max_x_point + 1):
            if Point(i, j) in set_points:
                pixels.append("#")
            elif i in target_x_range and j in target_y_range:
                pixels.append("T")
            else:
                pixels.append(".")
        pixels.append("\n")
    return "".join(pixels)


def launch_probe(
    velocity: Point, target_x_range: range, target_y_range: range
) -> tuple[list[Point], bool]:
    points = move_probe(Point(0, 0), velocity, min(target_y_range))
    # print(attempt_map(points, target_x_range, target_y_range))
    return points, any(p.x in target_x_range and p.z in target_y_range for p in points)


def solve_part_a() -> int:
    with open(FILE) as f:
        x_range, y_range = get_target_ranges(f)

    highest_y = 0
    # Chosen somewhat arbitrarily rather than find a nice way to terminate
    for j in range(100):
        for i in range(max(x_range) + 1):
            points, hit = launch_probe(Point(i, j), x_range, y_range)
            if hit:
                highest_y = max(p.z for p in points)
                break
    return highest_y


def solve_part_b() -> int:
    with open(FILE) as f:
        x_range, y_range = get_target_ranges(f)

    hit_velocities = []
    # Chosen somewhat arbitrarily rather than find a nice way to terminate
    for j in range(min(y_range), 100):
        for i in range(max(x_range) + 1):
            _, hit = launch_probe(Point(i, j), x_range, y_range)
            if hit:
                hit_velocities.append(Point(i, j))
    return len(hit_velocities)


def run():
    print(solve_part_a())
    print(solve_part_b())
