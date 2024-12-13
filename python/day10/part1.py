from collections import deque, namedtuple
from typing import Deque, List, Set

Point = namedtuple("Point", ["row", "col"])
Map = List[List[int]]


def parse(filename: str) -> Map:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    topo_map: Map = []
    for line in data:
        row: List[int] = [int(char) for char in line]
        topo_map.append(row)

    return topo_map


def solve(topo_map: Map) -> int:
    # get trailheads:
    trailheads: List[Point] = []
    for row, line in enumerate(topo_map):
        for col, trail in enumerate(line):
            if trail == 0:
                trailheads.append(Point(row, col))

    score: int = 0
    for trailhead in trailheads:
        # BFS init
        queue: Deque[Point] = deque([trailhead])
        visited: Set[Point] = set([trailhead])

        while queue:
            trailhead = queue.popleft()
            slope: int = topo_map[trailhead.row][trailhead.col]
            if slope == 9:
                score += 1
                continue

            for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row: int = trailhead.row + step_row
                new_col: int = trailhead.col + step_col

                if 0 <= new_row < len(topo_map) and 0 <= new_col < len(topo_map[0]):
                    new_slope: int = topo_map[new_row][new_col]
                    if new_slope == slope + 1 and (new_row, new_col) not in visited:
                        queue.append(Point(new_row, new_col))
                        visited.add(Point(new_row, new_col))

    return score


def solution(filename: str) -> int:
    topo_map: Map = parse(filename)
    return solve(topo_map)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 0
    print(solution("./input.txt"))  # 0
