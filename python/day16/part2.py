import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()
    return data


def solve(grid: List[str]) -> int:

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


    costs = defaultdict(lambda: float("inf"))
    costs[(start_row, start_col, 0, 1)] = 0
    prev = defaultdict(lambda: set())
    queue = deque([(start_row, start_col, 0, 1, 0)])

    while queue:
        row, col, dir_row, dir_col, cost = queue.popleft()

        for row_step, col_step in [(dir_row, dir_col), (dir_col, -dir_row), (-dir_col, dir_row)]:
            new_row = row + row_step
            new_col = col + col_step

            if grid[new_row][new_col] == "#":
                continue

            if (row_step, col_step) == (dir_row, dir_col):
                new_cost = cost + 1
            else:
                new_row, new_col = row, col
                new_cost = cost + 1000

            if new_cost < costs[(new_row, new_col, row_step, col_step)]:
                costs[(new_row, new_col, row_step, col_step)] = new_cost
                prev[(new_row, new_col, row_step, col_step)] = set([(row, col, dir_row, dir_col)])
                queue.append((new_row, new_col, row_step, col_step, new_cost))
            elif new_cost == costs[(new_row, new_col, row_step, col_step)]:
                prev[(new_row, new_col, row_step, col_step)].add((row, col, dir_row, dir_col))


    min_score = min(costs[(end_row, end_col, rd, cd)] for rd, cd in [(0, 1), (0, -1), (1, 0), (-1, 0)])
    min_ends = [(end_row, end_col, rd, cd) for rd, cd in [(0, 1), (0, -1), (1, 0), (-1, 0)] if costs[(end_row, end_col, rd, cd)] == min_score]

    # reverse walk
    queue = deque(min_ends)
    good_seats_positions = set(min_ends)

    while queue:
        end = queue.pop()
        for seat in prev[end]:
            if seat not in good_seats_positions:
                queue.append(seat)
                good_seats_positions.add(seat)

    good_seats = {(r, c) for r, c, _, _ in good_seats_positions}

    return len(good_seats)

def solution(filename: str) -> int:
    data: List[str] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example1.txt"))   # 45
    print(solution("./example2.txt"))   # 64
    print(solution("./input.txt"))  # 559
