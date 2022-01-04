from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Optional, TextIO

FILE = "solutions/day_06/input.txt"
TEST_FILE = "solutions/day_06/test_input.txt"


@dataclass(frozen=True)
class Fish:
    counter: int

    def pass_time(self) -> tuple[Fish, Optional[Fish]]:
        if self.counter == 0:
            return Fish(6), Fish(8)
        return Fish(self.counter - 1), None


def parse_fish(f: TextIO) -> list[Fish]:
    fish_str = f.readline().rstrip()
    return [Fish(int(n)) for n in fish_str.split(",")]


def fish_at_day_n(n: int, fishes: Iterable[Fish]) -> int:
    day = 0
    fish_counts = Counter(fishes)
    while day < n:
        new_counts: Counter[Fish] = Counter()
        for fish, count in fish_counts.items():
            fish_updated, maybe_new_fish = fish.pass_time()
            new_counts[fish_updated] += count
            if maybe_new_fish is not None:
                new_counts[maybe_new_fish] += count
        fish_counts = new_counts
        day += 1
    return fish_counts.total()


def solve_part_a() -> int:
    with open(FILE) as f:
        fishes = parse_fish(f)
    return fish_at_day_n(80, fishes)


def solve_part_b() -> int:
    with open(FILE) as f:
        fishes = parse_fish(f)
    return fish_at_day_n(256, fishes)


def run():
    print(solve_part_a())
    print(solve_part_b())
