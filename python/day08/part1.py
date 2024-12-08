from collections import defaultdict
from itertools import combinations
from typing import DefaultDict, List, NamedTuple, Set, Tuple


class Point(NamedTuple):
    x: int
    y: int


Antinode = Point
Antinodes = Set[Point]
Antenas = DefaultDict[str, Set[Point]]


def parse(filename: str) -> Tuple[Antenas, int, int]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    rows, cols = len(data), len(data[0])
    antenas: Antenas = defaultdict(set)

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char not in [".", "#"]:  # support example data
                antenas[char].add(Point(x, y))

    return antenas, rows, cols


def solve(antenas: Antenas, rows: int, cols: int) -> int:
    antinodes: Antinodes = set()
    for _antena_id, positions in antenas.items():
        for antena1, antena2 in combinations(positions, 2):

            dx: int = antena1.x - antena2.x
            dy: int = antena1.y - antena2.y

            # first antinode
            antinode: Antinode = Antinode(antena1.x + dx, antena1.y + dy)
            if 0 <= antinode.x < rows and 0 <= antinode.y < cols:
                antinodes.add(antinode)

            # second antinode
            antinode = Antinode(antena2.x - dx, antena2.y - dy)
            if 0 <= antinode.x < rows and 0 <= antinode.y < cols:
                antinodes.add(antinode)

    return len(antinodes)


def solution(filename: str) -> int:
    antenas, rows, cols = parse(filename)
    return solve(antenas, rows, cols)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 361
