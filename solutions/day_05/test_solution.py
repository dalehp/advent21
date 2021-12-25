import pytest

from solutions.day_05.solution import Pipe, Point


@pytest.mark.parametrize(
    "pipe,points",
    [
        # Vertical Pipe
        (Pipe(Point(1, 1), Point(1, 3)), [Point(1, 1), Point(1, 2), Point(1, 3)]),
        # Horizontal Pipe
        (Pipe(Point(9, 7), Point(7, 7)), [Point(9, 7), Point(8, 7), Point(7, 7)]),
        # Diagonal Pipe
        (Pipe(Point(1, 1), Point(3, 3)), [Point(1, 1), Point(2, 2), Point(3, 3)]),
    ],
)
def test_points(pipe, points):
    assert list(pipe.points(include_diagonal=True)) == points
