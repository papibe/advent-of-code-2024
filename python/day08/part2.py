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

            antinodes.add(antena1)

            delta_x: int = antena1.x - antena2.x
            delta_y: int = antena1.y - antena2.y

            # go through the line formed by antena1 and antena2
            for dx, dy in [(delta_x, delta_y), (-delta_x, -delta_y)]:
                antinode: Antinode = Antinode(antena1.x + dx, antena1.y + dy)

                while 0 <= antinode.x < rows and 0 <= antinode.y < cols:
                    antinodes.add(antinode)
                    antinode = Antinode(antinode.x + dx, antinode.y + dy)

    return len(antinodes)


def solution(filename: str) -> int:
    antenas, rows, cols = parse(filename)
    return solve(antenas, rows, cols)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 1249
