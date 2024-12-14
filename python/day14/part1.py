import re
from dataclasses import dataclass
from typing import List


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
    # move robots 100 times
    for _ in range(100):
        for r in robots:
            r.col = (r.col + r.vcol) % cols
            r.row = (r.row + r.vrow) % rows

    # count robots in all 4 quadrants
    q1 = q2 = q3 = q4 = 0
    for r in robots:
        if r.row < rows // 2 and r.col < cols // 2:
            q1 += 1

        elif r.row < rows // 2 and r.col > cols // 2:
            q2 += 1

        elif r.row > rows // 2 and r.col < cols // 2:
            q3 += 1

        elif r.row > rows // 2 and r.col > cols // 2:
            q4 += 1

    return q1 * q2 * q3 * q4


def solution(filename: str, rows: int, cols: int) -> int:
    data: List[Robot] = parse(filename)
    return solve(data, rows, cols)


if __name__ == "__main__":
    print(solution("./example.txt", 7, 11))  # 12
    print(solution("./input.txt", 103, 101))  # 224357412
