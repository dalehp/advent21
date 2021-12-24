import copy
from collections import Counter
from typing import Optional, TextIO

Calls = list[int]
RawBoard = list[list[int]]
Position = tuple[int, int]

FILE = "solutions/day_04/input.txt"


class Board:
    def __init__(self, raw_board: RawBoard):
        self._number_position_map: dict[int, Position] = {}
        self._positions_checked: dict[Position, int] = {}
        self._x_counts: Counter[int] = Counter()
        self._y_counts: Counter[int] = Counter()
        self._last_called = 0
        self._won = False

        for y, line in enumerate(raw_board):
            for x, number in enumerate(line):
                self._number_position_map[number] = (x, y)

        if x != y:
            raise ValueError("Board must be square")
        self._board_size = x

    def check_number(self, n: int) -> Optional[int]:
        pos = self._number_position_map.get(n)
        self._last_called = n
        if pos is None:
            return None
        self._positions_checked[pos] = n
        x, y = pos
        self._x_counts[x] += 1
        self._y_counts[y] += 1

        return self._check_win()

    def _is_win(self) -> bool:
        return any(
            count == self._board_size + 1 for _, count in self._x_counts.items()
        ) or any(count == self._board_size + 1 for _, count in self._y_counts.items())

    def _check_win(self) -> Optional[int]:
        if not self._is_win() or self._won:
            return None

        self._won = True

        checked_numbers = set(self._positions_checked.values())
        unchecked_numbers = self._number_position_map.keys() - checked_numbers
        return sum(unchecked_numbers) * self._last_called


def parse_bingo_file(f: TextIO) -> tuple[Calls, list[Board]]:
    calls_str = f.readline().rstrip()
    calls = [int(n) for n in calls_str.split(",")]
    # Skip empty line
    next(f)

    raw_boards: list[RawBoard] = []
    board: RawBoard = []
    for line in f:
        if not line.rstrip():
            raw_boards.append(copy.copy(board))
            board.clear()
            continue
        b_line = [int(x) for x in line.split()]
        board.append(b_line)

    boards = [Board(raw_board) for raw_board in raw_boards]

    return calls, boards


def solve_part_a() -> int:
    with open(FILE) as f:
        calls, boards = parse_bingo_file(f)
    for call in calls:
        for board in boards:
            win = board.check_number(call)
            if win is not None:
                return win
    raise ValueError("No boards won")


def solve_part_b() -> int:
    with open(FILE) as f:
        calls, boards = parse_bingo_file(f)

    last_win = None
    for call in calls:
        for board in boards:
            win = board.check_number(call)
            if win is not None:
                last_win = win
    return last_win


if __name__ == "__main__":
    print(solve_part_a())
    print(solve_part_b())
