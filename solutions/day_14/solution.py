from typing import  TextIO
from collections import Counter

FILE = "solutions/day_14/input.txt"
TEST_FILE = "solutions/day_14/test_input.txt"


PolymerPair = tuple[str, str]
Polymers = Counter[PolymerPair]
Translations = dict[PolymerPair, tuple[PolymerPair, PolymerPair]]


def load_polymers_and_translations(f: TextIO) -> tuple[Polymers, Translations, str]:
    polymers = []
    polymer_str = f.readline().rstrip()
    last_polymer = polymer_str[-1]
    for c, d in zip(polymer_str, polymer_str[1:]):
        polymers.append((c, d))

    # Skip empty line
    f.readline()

    translations = {}
    for line in f:
        input_p, output_p = line.rstrip().split(" -> ")
        input_p_1, input_p_2 = list(input_p)
        translations[(input_p_1, input_p_2)] = ((input_p_1, output_p), (output_p, input_p_2))

    return Counter(polymers), translations, last_polymer

def step_polymers(polymers: Polymers, translations: Translations) -> Polymers:
    new_polymers: Counter[PolymerPair] = Counter()
    for pair, count in polymers.items():
        new_pair_1, new_pair_2 = translations[pair]
        new_polymers[new_pair_1] += count
        new_polymers[new_pair_2] += count
    return new_polymers

def convert_pairs_to_singles(polymers: Polymers, last_polymer: str) -> Counter[str]:
    single_counts = Counter([last_polymer])
    for (first_poly, _), count in polymers.items():
        single_counts[first_poly] += count
    return single_counts

def solve_for_n_steps(n: int) -> int:
    with open(FILE) as f:
        polymers, translations, last_polymer = load_polymers_and_translations(f)

    for i in range(n):
        polymers = step_polymers(polymers, translations)

    counts = convert_pairs_to_singles(polymers, last_polymer)
    most_common = counts.most_common()
    _, most_common_count = most_common[0]
    _, least_common_count = most_common[-1]
    return most_common_count - least_common_count

def solve_part_a() -> int:
    return solve_for_n_steps(10)

def solve_part_b() -> int:
    return solve_for_n_steps(40)

def run():
    print(solve_part_a())
    print(solve_part_b())
