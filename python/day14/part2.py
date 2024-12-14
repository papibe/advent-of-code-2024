import re
from dataclasses import dataclass
from typing import List

XMAS_FRAME: str = "+++++++++++++++++++++++++++++++"


@dataclass
class Robot:
    col: int
    row: int
    vcol: int
    vrow: int


def parse(filename: str) -> List[Robot]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    re_line: str = r"p=(\d+),(\d+) v=([0-9\-]+),([0-9\-]+)"

    robots: List[Robot] = []

    for line in data:
        matches = re.match(re_line, line)
        assert matches is not None

        col: int = int(matches.group(1))
        row: int = int(matches.group(2))
        vcol: int = int(matches.group(3))
        vrow: int = int(matches.group(4))

        robots.append(Robot(col, row, vcol, vrow))

    return robots


def solve(robots: List[Robot], rows: int, cols: int) -> int:

    # prep grid for printing
    grid: List[List[str]] = []
    for _ in range(rows):
        grid.append(["." for col in range(cols)])

    # iterate over a big number and look for tree
    for second in range(1, 10_000):
        for r in robots:
            r.col = (r.col + r.vcol) % cols
            r.row = (r.row + r.vrow) % rows

        for r in robots:
            grid[r.row][r.col] = "+"

        for row in grid:
            if XMAS_FRAME in "".join([str(item) for item in row]):
                return second

        for r in robots:
            grid[r.row][r.col] = "."

    return 0


def solution(filename: str, rows: int, cols: int) -> int:
    data: List[Robot] = parse(filename)
    return solve(data, rows, cols)


if __name__ == "__main__":
    print(solution("./input.txt", 103, 101))  # 7083
