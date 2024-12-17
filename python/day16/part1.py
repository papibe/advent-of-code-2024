import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()
    return data


def solve(grid: List[str]) -> int:

    costs = []
    for _ in range(len(grid)):
        costs.append([float("inf") for _ in range(len(grid[0]))])

    # print(len(costs), len(costs[0]))

    start_row: int
    start_col: int
    end_row: int
    end_col: int
    # find start and end
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == "S":
                start_row = row
                start_col = col
            elif cell == "E":
                end_row = row
                end_col = col

    # print(start_row, start_col, end_row, end_col)

    queue = deque([(start_row, start_col, 0, 1,0)])
    visited = set([(start_row, start_col)])

    while queue:
        row, col, dir_row, dir_col, cost = queue.popleft()
        # if row == end_row and col == end_col:
        #     return cost

        for row_step, col_step in [(dir_row, dir_col), (dir_col, -dir_row), (-dir_col, dir_row)]:
            new_row = row + row_step
            new_col = col + col_step
            # print(f"{new_row = }, {new_col =}")

            if grid[new_row][new_col] == "#":
                continue

            if (row_step, col_step) == (dir_row, dir_col):
                added_cost = 1
            else:
                added_cost = 1001

            new_cost = cost + added_cost

            if new_cost < costs[new_row][new_col]:
                costs[new_row][new_col] = new_cost
                queue.append((new_row, new_col, row_step, col_step, new_cost))


    return costs[end_row][end_col]


def solution(filename: str) -> int:
    data: List[str] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example1.txt"))    # 0
    print(solution("./example2.txt"))    # 0
    print(solution("./input.txt"))  # 0
