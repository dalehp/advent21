import pytest

from solutions.day_04 import solution

BOARD = [
    [1, 4, 9],
    [22, 5, 19],
    [21, 2, 34],
]


def test_check_number():
    board = solution.Board(BOARD)
    board.check_number(34)
    assert board._positions_checked == {(2, 2): 34}
    assert board._x_counts[2] == 1
    assert board._y_counts[2] == 1


@pytest.mark.parametrize(
    "calls,win_value",
    [
        # Vertical Win
        ((1, 22, 5, 21), 1428),
        # Horizontal Win
        ((1, 5, 21, 4, 9), 693),
        # Longest possible win
        ((1, 5, 34, 9, 21, 2), 90),
    ],
)
def test_check_win(calls, win_value):
    board = solution.Board(BOARD)
    for call in calls:
        assert board._check_win() == None
        board.check_number(call)

    assert board._check_win() == win_value
