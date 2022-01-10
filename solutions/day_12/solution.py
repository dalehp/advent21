from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, TextIO

FILE = "solutions/day_12/input.txt"
TEST_FILE = "solutions/day_12/test_input.txt"


class NodeType(Enum):
    START = auto()
    END = auto()
    SMALL = auto()
    BIG = auto()

@dataclass
class Node:
    name: str
    children: list[Node] = field(default_factory=list)

    def __repr__(self) -> str:
        return self.name

    @property
    def node_type(self) -> NodeType:
        if self.name == "start":
            return NodeType.START
        elif self.name == "end":
            return NodeType.END
        elif self.name.isupper():
            return NodeType.BIG
        elif self.name.islower():
            return NodeType.SMALL
        raise ValueError(f"Invalid node name {self.name}")

Graph = dict[str, Node]

def load_edges_from_file(f: TextIO) -> list[tuple[str, str]]:
    edges = []
    for line in f:
        l, _, r = line.rstrip().partition('-')
        edges.append((l, r))
    return edges

def construct_graph_from_edges(edges: list[tuple[str, str]]) -> Graph:
    graph = {}
    for l, r in edges:
        if l not in graph:
            graph[l] = Node(l)
        if r not in graph:
            graph[r] = Node(r)

        graph[l].children.append(graph[r])
        graph[r].children.append(graph[l])
    return graph

def can_visit_node_a(node: Node, visited: Counter[str]) -> bool:
    return node.node_type is NodeType.BIG or node.name not in visited

def can_visit_node_b(node: Node, visited: Counter[str]) -> bool:
    if node.node_type is NodeType.BIG:
        return True
    elif node.node_type is NodeType.SMALL:
        if all(count == 1 for node, count in visited.items() if Node(node).node_type is NodeType.SMALL):
            return True
    return node.name not in visited




def count_paths_through_graph(graph: Graph, visit_fn: Callable) -> int:
    paths = [[graph['start']]]
    completed = []
    while paths:
        path = paths.pop()
        visited = Counter([p.name for p in path])
        for next_node in path[-1].children:
            if not visit_fn(next_node, visited):
                continue
            if next_node.node_type is NodeType.END:
                completed.append(path + [next_node])
                continue
            paths.append(path + [next_node])
    return len(completed)


def solve_part_a() -> int:
    with open(FILE) as f:
        edges = load_edges_from_file(f)
    graph = construct_graph_from_edges(edges)
    return count_paths_through_graph(graph, can_visit_node_a)


def solve_part_b() -> int:
    with open(FILE) as f:
        edges = load_edges_from_file(f)
    graph = construct_graph_from_edges(edges)
    return count_paths_through_graph(graph, can_visit_node_b)


def run():
    print(solve_part_a())
    print(solve_part_b())
