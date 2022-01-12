import heapq
from dataclasses import dataclass, field
from typing import Any

from solutions.common import IntGrid, Point, adjacent_points_and_values

FILE = "solutions/day_15/input.txt"
TEST_FILE = "solutions/day_15/test_input.txt"


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def shortest_path(grid: IntGrid) -> int:
    """
    Dijkstra's algorithm, using the notation from
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    start, finish = grid.bounds
    q = [PrioritizedItem(0, start)]
    prev = {}
    dist = {start: 0}

    while q:
        u_item = heapq.heappop(q)
        u = u_item.item
        dist_u = u_item.priority
        if dist[u] != dist_u:
            continue
        if u == finish:
            return dist_u

        for v, len_u_v in adjacent_points_and_values(grid, u):
            alt = dist_u + len_u_v
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(q, PrioritizedItem(alt, v))
    raise RuntimeError("Never reached goal")


def expand_grid(grid: IntGrid) -> IntGrid:
    base_grid = grid.grid
    _, mp = grid.bounds
    incr_x = mp.x + 1
    incr_z = mp.z + 1
    for i in range(5):
        for j in range(5):
            new_grid_dict = {
                Point(p.x + incr_x * i, p.z + incr_z * j): (v + i + j - 1) % 9 + 1
                for p, v in base_grid.items()
            }
            grid += IntGrid.from_dict(new_grid_dict)
    return grid


def solve_part_a() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)
    return shortest_path(grid)


def solve_part_b() -> int:
    with open(FILE) as f:
        grid = IntGrid.from_file(f)
    big_grid = expand_grid(grid)
    return shortest_path(big_grid)


def run():
    print(solve_part_a())
    print(solve_part_b())
