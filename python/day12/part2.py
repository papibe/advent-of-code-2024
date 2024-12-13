from collections import deque, namedtuple
from typing import Deque, List, Set

Garden = List[str]
Point = namedtuple("Point", ["row", "col"])
Direction = Point
Region = Set[Point]
Regions = List[Region]
Edge = namedtuple("Edge", ["point", "direction"])
Edges = List[Edge]


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


def find(i: int, parent: List[int]) -> int:
    """find for union/find/disjoint-sets"""
    if parent[i] == i:
        return i

    return find(parent[i], parent)


def union(i: int, j: int, parent: List[int]) -> None:
    """union for union/find/disjoint-sets"""
    i_root = find(i, parent)
    j_root = find(j, parent)
    parent[i_root] = j_root


def are_neighbors(edge1: Point, edge2: Point) -> bool:
    """determine if to edges (points) are neighbors"""
    (row1, col1) = edge1
    (row2, col2) = edge2
    for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row = row1 + step_row
        new_col = col1 + step_col
        if (new_row, new_col) == (row2, col2):
            return True

    return False


def get_sides(members: Region) -> int:
    """get sides of a region"""
    edges: Edges = []
    for member in members:
        row, col = member

        for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = row + step_row
            new_col = col + step_col
            if (new_row, new_col) not in members:
                edges.append(Edge(Point(row, col), Direction(step_row, step_col)))

    # create relationships for a union/find algo
    parent = list(range(len(edges)))

    for i in range(len(parent)):
        for j in range(i + 1, len(parent)):
            if (
                are_neighbors(edges[i].point, edges[j].point)
                and edges[i].direction == edges[j].direction
            ):
                union(i, j, parent)

    # get disjoing sets, or sides
    sides: Set[int] = set()
    for i in parent:
        sides.add(find(i, parent))

    return len(sides)


def solve(garden: Garden) -> int:
    regions: Regions = get_regions(garden)

    fence_cost: int = 0
    for members in regions:
        fence_cost += get_sides(members) * len(members)

    return fence_cost


def solution(filename: str) -> int:
    garden: Garden = parse(filename)
    return solve(garden)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 899196
