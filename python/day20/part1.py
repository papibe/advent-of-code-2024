import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


START: str = "S"
END: str = "E"
WALL: str = "#"
SPACE: str = "."


def parse(filename: str) -> Tuple[List[str], int, int, int, int]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()


    grid = []
    for line in data:
        grid.append([char for char in line])

    # print(grid)

    start_row: int
    start_col: int
    end_row: int
    end_col: int

    # find start and end
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == START:
                start_row = row
                start_col = col
            elif cell == END:
                end_row = row
                end_col = col

    return grid, start_row, start_col, end_row, end_col

def run(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int
) -> int:
    # BFS setup
    queue: Deque[Tuple[int, int, int, int, int]] = deque(
        [(start_row, start_col, 0)]
    )
    visited = set([(start_row, start_col)])

    # BFS
    while queue:
        row, col, cost = queue.popleft()

        if row == end_row and col == end_col:
            return cost

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[new_row][new_col] == WALL:
                    continue

                if (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, cost + 1))
                    visited.add((new_row, new_col))
    return -1

def solve(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int
) -> int:
    main_result = run(grid, start_row, start_col, end_row, end_col)
    # print(f"{main_result}")
    results = []
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == WALL:
                grid[row][col] = SPACE
                result = run(grid, start_row, start_col, end_row, end_col)
                grid[row][col] = WALL

                results.append(main_result - result)
    # print(results)
    return len([result for result in results if result >= 100])



def solution(filename: str) -> int:
    grid, start_row, start_col, end_row, end_col = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col)


if __name__ == "__main__":
    # it takes 3m28s
    print(solution("./input.txt"))  # 1417
