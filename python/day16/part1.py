from collections import deque
from typing import Deque, List, Tuple

START: str = "S"
END: str = "E"
WALL: str = "#"


def parse(filename: str) -> Tuple[List[str], int, int, int, int]:
    with open(filename, "r") as fp:
        grid: List[str] = fp.read().splitlines()

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


def solve(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int
) -> int:
    # setup costs for dijkstra
    costs: List[List[int]] = []
    for _ in range(len(grid)):
        costs.append([float("inf") for _ in range(len(grid[0]))])  # type: ignore

    queue: Deque[Tuple[int, int, int, int, int]] = deque(
        [(start_row, start_col, 0, 1, 0)]
    )

    # Dijkstra
    while queue:
        row, col, dir_row, dir_col, cost = queue.popleft()

        for row_step, col_step in [
            (dir_row, dir_col),
            (dir_col, -dir_row),
            (-dir_col, dir_row),
        ]:
            new_row: int = row + row_step
            new_col: int = col + col_step

            if grid[new_row][new_col] == WALL:
                continue

            new_cost: int
            if (row_step, col_step) == (dir_row, dir_col):
                new_cost = cost + 1
            else:
                new_cost = cost + 1001

            if new_cost < costs[new_row][new_col]:
                costs[new_row][new_col] = new_cost
                queue.append((new_row, new_col, row_step, col_step, new_cost))

    return costs[end_row][end_col]


def solution(filename: str) -> int:
    grid, start_row, start_col, end_row, end_col = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 7036
    print(solution("./example2.txt"))  # 11048
    print(solution("./input.txt"))  # 102488
