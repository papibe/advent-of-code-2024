from collections import namedtuple
from typing import List, Set

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

    rating: int = 0

    for trailhead in trailheads:

        def dfs(trailhead: Point, visited: Set[Point]) -> int:
            slope: int = topo_map[trailhead.row][trailhead.col]

            if slope == 9:
                return 1

            trail_rating: int = 0
            for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row: int = trailhead.row + step_row
                new_col: int = trailhead.col + step_col

                if 0 <= new_row < len(topo_map) and 0 <= new_col < len(topo_map[0]):
                    new_slope: int = topo_map[new_row][new_col]

                    if new_slope == slope + 1 and (new_row, new_col) not in visited:
                        visited.add(Point(new_row, new_col))
                        trail_rating += dfs(Point(new_row, new_col), visited)
                        visited.remove(Point(new_row, new_col))

            return trail_rating

        visited: Set[Point] = set([trailhead])
        rating += dfs(trailhead, visited)

    return rating


def solution(filename: str) -> int:
    data: Map = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 13
    print(solution("./example.txt"))  # 81
    print(solution("./input.txt"))  # 1380
