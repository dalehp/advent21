from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, TextIO

FILE = "solutions/day_08/input.txt"
TEST_FILE = "solutions/day_08/test_input.txt"

"""
 hhhh
i    j
i    j
 kkkk
l    m
l    m
 nnnn
"""

NUMBERS_TO_SEGMENTS = {
    0: frozenset("hijlmn"),
    1: frozenset("jm"),
    2: frozenset("hjkln"),
    3: frozenset("hjkmn"),
    4: frozenset("ikjm"),
    5: frozenset("hikmn"),
    6: frozenset("hiklmn"),
    7: frozenset("hjm"),
    8: frozenset("hijklmn"),
    9: frozenset("hijkmn"),
}

SEGMENTS_TO_NUMBERS = {s: n for n, s in NUMBERS_TO_SEGMENTS.items()}


class Display:
    def __init__(self, test_digits: tuple[str, ...], output_digits: tuple[str, ...]):
        self.test_digits = test_digits
        self.output_digits = output_digits

        segments_to_solve = "abcdefg"
        actual_segments = "hijklmn"
        numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.possible_segments = {s: set(actual_segments) for s in segments_to_solve}
        self.possible_numbers = {}
        for d in self.test_digits:
            self.possible_numbers[d] = set(
                n for n in numbers if len(d) == len(NUMBERS_TO_SEGMENTS[n])
            )
        self.solve()

    def _update_possible_segments(self):
        for digit, numbers in self.possible_numbers.items():
            for segment in digit:
                possible_segments = set.union(
                    *[set(NUMBERS_TO_SEGMENTS[n]) for n in numbers]
                )
                self.possible_segments[segment] &= possible_segments

        options = list(self.possible_segments.values())
        for option in options:
            if len(option) == options.count(option):
                for segment, possibilities in self.possible_segments.items():
                    if possibilities != option:
                        possibilities -= option

    def _update_possible_numbers(self):
        for digit, numbers in self.possible_numbers.items():
            impossible = set()
            for number in numbers:
                possible_segments = set.union(
                    *[self.possible_segments[s] for s in digit]
                )
                if not possible_segments.issuperset(NUMBERS_TO_SEGMENTS[number]):
                    impossible.add(number)

                # for segment, options in self.possible_segments.values:
                #     if all(option in digit for option in options) and not
                options = list(self.possible_segments.values())
                known = defaultdict(set)
                for segment, possibilities in self.possible_segments.items():
                    if len(possibilities) == options.count(possibilities):
                        known[frozenset(possibilities)].add(segment)

                for known_poss, known_segments in known.items():
                    if all(
                        s in digit for s in known_segments
                    ) and not NUMBERS_TO_SEGMENTS[number].issuperset(known_poss):
                        impossible.add(number)

            numbers -= impossible

    def solve(self) -> int:
        self._update_possible_segments()
        self._update_possible_segments()
        self._update_possible_numbers()

        real_outputs = []
        frozen_possibles = {frozenset(d): ns for d, ns in self.possible_numbers.items()}
        for digit in self.output_digits:
            (real_digit,) = frozen_possibles[frozenset(digit)]
            real_outputs.append(real_digit)
        return int("".join([str(o) for o in real_outputs]))


def yield_displays(file: TextIO) -> Iterator[Display]:
    for line in file:
        tests, outputs = line.rstrip().split("|")
        yield (
            Display(
                test_digits=tuple(tests.split()),
                output_digits=tuple(outputs.split()),
            )
        )


def is_number_1_4_7_or_8(segments: str) -> bool:
    return len(segments) in (2, 3, 4, 7)


def solve_part_a() -> int:
    ones_fours_sevens_and_eights = 0
    with open(FILE) as f:
        for display in yield_displays(f):
            for digit in display.output_digits:
                if is_number_1_4_7_or_8(digit):
                    ones_fours_sevens_and_eights += 1
    return ones_fours_sevens_and_eights


def solve_part_b() -> int:
    total = 0
    with open(FILE) as f:
        for display in yield_displays(f):
            total += display.solve()
    return total


def run():
    print(solve_part_a())
    print(solve_part_b())
