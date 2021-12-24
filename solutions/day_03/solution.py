import copy
from collections import defaultdict
from typing import Iterator, Iterable, Sequence, TextIO

FILE = "solutions/day_03/input.txt"
TEST_FILE = "solutions/day_03/test_input.txt"


def iterate_byte_tuples(f: TextIO) -> Iterator[tuple[int, ...]]:
    for line in f:
        yield tuple(int(x) for x in line.strip())


def byte_sequence_to_int(byte_tuple: Sequence[int]) -> int:
    string_tuple = [str(b) for b in byte_tuple]
    return int("".join(string_tuple), 2)


def convert_counts_to_gamma_epsilon(
    counts: defaultdict[int, int], total: int
) -> tuple[int, int]:
    gamma_bits = []
    epsilon_bits = []
    half_count = total // 2
    for i in range(len(counts)):
        count = counts[i]
        gamma_bits.append(1 if count > half_count else 0)
        epsilon_bits.append(0 if count > half_count else 1)
    return byte_sequence_to_int(gamma_bits), byte_sequence_to_int(epsilon_bits)


def solve_part_a():
    counts = defaultdict(int)
    with open(FILE) as f:
        for i, byte_tuple in enumerate(iterate_byte_tuples(f), 1):
            for j, bit in enumerate(byte_tuple):
                counts[j] += bit
    gamma, episilon = convert_counts_to_gamma_epsilon(counts, i)
    return gamma * episilon


def sum_bits_in_position(pos: int, byte_tuples: Iterable[tuple[int, ...]]) -> int:
    return sum(bt[pos] for bt in byte_tuples)


def calculate_oxygen(byte_tuples: Sequence[tuple[int, ...]]) -> int:
    pos = 0
    bts = copy.copy(byte_tuples)
    while (remaining := len(bts)) > 1:
        sum = sum_bits_in_position(pos, bts)
        winner = 1 if sum * 2 >= remaining else 0
        bts = [bt for bt in bts if bt[pos] == winner]
        pos += 1
    [result] = bts
    return byte_sequence_to_int(result)


def calculate_co2(byte_tuples: Sequence[tuple[int, ...]]) -> int:
    pos = 0
    bts = copy.copy(byte_tuples)
    while (remaining := len(bts)) > 1:
        sum = sum_bits_in_position(pos, bts)
        winner = 0 if sum * 2 >= remaining else 1
        bts = [bt for bt in bts if bt[pos] == winner]
        pos += 1
    [result] = bts
    return byte_sequence_to_int(result)


def solve_part_b():
    with open(FILE) as f:
        byte_tuples = list(iterate_byte_tuples(f))
    oxygen = calculate_oxygen(byte_tuples)
    co2 = calculate_co2(byte_tuples)
    return oxygen * co2


def run():
    print(solve_part_a())
    print(solve_part_b())
