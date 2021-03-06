from typing import Iterator, TextIO

FILE = "solutions/day_01/input.txt"


def yield_window_on_file(file: TextIO, length: int) -> Iterator[tuple[int, ...]]:
    buffer: list[int] = []
    for line in file:
        value = int(line.rstrip())
        buffer.append(value)
        if len(buffer) < length:
            continue
        yield tuple(buffer)
        buffer.pop(0)


def solve_part_a() -> int:
    depth_increase_count = 0
    with open(FILE) as f:
        for first, second in yield_window_on_file(f, 2):
            if second > first:
                depth_increase_count += 1
    return depth_increase_count


def solve_part_b() -> int:
    depth_increase_count = 0
    with open(FILE) as f, open(FILE) as g:
        # Offset second file by 1
        next(g)
        for first, second in zip(
            yield_window_on_file(f, 3), yield_window_on_file(g, 3)
        ):
            if sum(second) > sum(first):
                depth_increase_count += 1
    return depth_increase_count


def run():
    print(solve_part_a())
    print(solve_part_b())
