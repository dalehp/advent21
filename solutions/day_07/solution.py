from typing import Callable, TextIO

FILE = "solutions/day_07/input.txt"
TEST_FILE = "solutions/day_07/test_input.txt"

def get_crab_positions_from_file(f: TextIO) -> tuple[int, ...]:
    raw_crabs = f.readline().rstrip()
    return tuple(int(c) for c in raw_crabs.split(','))

def get_fuel_for_crabs(crabs: tuple[int, ...], position: int) -> int:
    return sum(abs(c - position) for c in crabs)

def get_non_linear_fuel(distance: int) -> int:
    return (distance * (distance + 1)) // 2

def get_refined_fuel(crabs: tuple[int, ...], position: int) -> int:
    """Calculates the non-linear fuel expended for part b"""
    return sum(get_non_linear_fuel(abs(c - position)) for c in crabs)

def solve(fuel_fn: Callable):
    with open(FILE) as f:
        crabs = get_crab_positions_from_file(f)

    min_position = min(crabs)
    max_position = max(crabs)

    lowest_fuel = float('inf')
    for position in range(min_position, max_position + 1):
        fuel = fuel_fn(crabs, position)
        lowest_fuel = min(lowest_fuel, fuel)

    return int(lowest_fuel)


def solve_part_a() -> int:
    return solve(get_fuel_for_crabs)

def solve_part_b() -> int:
    return solve(get_refined_fuel)

def run():
    print(solve_part_a())
    print(solve_part_b())