from collections import deque, namedtuple
from copy import deepcopy
from typing import Deque, FrozenSet, List, Set, Tuple

Point = namedtuple("Point", ["row", "col"])
Map = List[List[int]]


def parse(filename: str) -> Map:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    topop_map = []
    for line in data:
        row: List[int] = []
        for char in line:
            if char.isnumeric():
                row.append(int(char))
            else:
                row.append(-1)
        topop_map.append(row)

    return topop_map


def solve(topo_map: Map) -> int:
    # get trailheads:
    trailheads: List[Point] = []
    for row, line in enumerate(topo_map):
        for col, trail in enumerate(line):
            if trail == 0:
                trailheads.append(Point(row, col))

    score: int = 0
    rating: int = 0

    for trailhead in trailheads:
        # BFS init
        visited: Set[Point] = set([trailhead])
        queue: Deque[Tuple[Point, Set[Point]]] = deque([(trailhead, visited)])

        paths: Set[FrozenSet[Point]] = set()

        # BFS
        while queue:
            trailhead, visited = queue.popleft()
            slope: int = topo_map[trailhead.row][trailhead.col]

            if slope == 9:
                score += 1
                paths.add(frozenset(visited))
                continue

            for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row: int = trailhead.row + step_row
                new_col: int = trailhead.col + step_col

                if 0 <= new_row < len(topo_map) and 0 <= new_col < len(topo_map[0]):
                    new_slope: int = topo_map[new_row][new_col]
                    if new_slope == slope + 1 and (new_row, new_col) not in visited:
                        new_visited: Set[Point] = deepcopy(visited)
                        new_visited.add(Point(new_row, new_col))
                        queue.append((Point(new_row, new_col), new_visited))

        rating += len(paths)

    return rating


def solution(filename: str) -> int:
    topo_map: Map = parse(filename)
    return solve(topo_map)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 13
    print(solution("./example.txt"))  # 81
    print(solution("./input.txt"))  # 1380
