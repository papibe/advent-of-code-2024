from collections import deque, namedtuple
from typing import Deque, List, Set

Garden = List[str]
Point = namedtuple("Point", ["row", "col"])
Region = Set[Point]
Regions = List[Region]


def parse(filename: str) -> Garden:
    with open(filename, "r") as fp:
        garden: Garden = fp.read().splitlines()

    return garden


def get_regions(garden: Garden) -> Regions:
    """get regions from the garden"""
    assigned_to_zone: Set[Point] = set()
    regions: Regions = []

    for start_row, line in enumerate(garden):
        for start_col, item in enumerate(line):

            kind: str = item

            if (start_row, start_col) in assigned_to_zone:
                continue

            region: Region = set([Point(start_row, start_col)])
            assigned_to_zone.add(Point(start_row, start_col))

            queue: Deque[Point] = deque([Point(start_row, start_col)])
            visited: Set[Point] = set([Point(start_row, start_col)])

            # BFS
            while queue:
                row, col = queue.popleft()
                if garden[row][col] != kind:
                    continue

                region.add(Point(row, col))
                assigned_to_zone.add(Point(row, col))

                for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_row: int = row + step_row
                    new_col: int = col + step_col

                    if 0 <= new_row < len(garden) and 0 <= new_col < len(garden[0]):
                        if (new_row, new_col) not in visited:
                            queue.append(Point(new_row, new_col))
                            visited.add(Point(new_row, new_col))

            regions.append(region)

    return regions


def get_perimeter(members: Region) -> int:
    """get perimeter of a region"""
    perimeter: int = 0

    for member in members:
        individual_perimeter: int = 4
        row, col = member
        for new_row, new_col in [
            (row, col + 1),
            (row, col - 1),
            (row + 1, col),
            (row - 1, col),
        ]:
            if (new_row, new_col) in members:
                individual_perimeter -= 1

        perimeter += individual_perimeter

    return perimeter


def solve(garden: Garden) -> int:
    regions: Regions = get_regions(garden)

    fence_cost: int = 0
    for members in regions:
        fence_cost += get_perimeter(members) * len(members)

    return fence_cost


def solution(filename: str) -> int:
    garden: Garden = parse(filename)
    return solve(garden)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 1485656
