import statistics

FILE = "solutions/day_10/input.txt"
TEST_FILE = "solutions/day_10/test_input.txt"

OPEN_TO_CLOSE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
CLOSE_TO_OPEN = {r: l for l, r in OPEN_TO_CLOSE.items()}
CLOSE_TO_CORRUPTION_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
OPEN_TO_COMPLETE_SCORE = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def corruption_score(line: str) -> int:
    open_brackets = []
    for bracket in line:
        if bracket in OPEN_TO_CLOSE:
            open_brackets.append(bracket)
        elif matched := CLOSE_TO_OPEN.get(bracket):
            if matched != open_brackets.pop():
                return CLOSE_TO_CORRUPTION_SCORE[bracket]
        else:
            raise ValueError(f"Found unexpected symbol {bracket}")
    return 0


def _calculate_incomplete_score(open_brackets: list[str]) -> int:
    score = 0
    for bracket in open_brackets[::-1]:
        score *= 5
        score += OPEN_TO_COMPLETE_SCORE[bracket]
    return score


def incomplete_score(line: str) -> int:
    open_brackets = []
    for bracket in line:
        if bracket in OPEN_TO_CLOSE:
            open_brackets.append(bracket)
        elif matched := CLOSE_TO_OPEN.get(bracket):
            if matched != open_brackets.pop():
                return 0
        else:
            raise ValueError(f"Found unexpected symbol {bracket}")

    return _calculate_incomplete_score(open_brackets)


def solve_part_a() -> int:
    score = 0
    with open(FILE) as f:
        for line in f:
            score += corruption_score(line.rstrip())
    return score


def solve_part_b() -> int:
    scores = []
    with open(FILE) as f:
        for line in f:
            score = incomplete_score(line.rstrip())
            if score != 0:
                scores.append(score)
    median = statistics.median(scores)
    if not isinstance(median, int):
        raise ValueError("Odd number of scores, error in input or code")
    return median


def run():
    print(solve_part_a())
    print(solve_part_b())
