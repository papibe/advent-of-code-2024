from typing import List, Set, Tuple

Grid = Set[Tuple[int, int]]
State = Set[Tuple[int, int, int, int]]

INITIAL_DIRECTION: Tuple[int, int] = (-1, 0)
SPACE: str = "."
GUARD: str = "^"
OBSTABLE: str = "#"


def parse(filename: str) -> Tuple[int, int, int, int, Grid]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    # build grid and get guard initial position
    grid: Grid = set()
    initial_row: int
    initial_col: int
    row_size: int = len(data)
    col_size: int = len(data[0])

    for row, line in enumerate(data):
        for col, cell in enumerate(line):
            # record initial position and replce it with space
            if cell == GUARD:
                initial_row = row
                initial_col = col
            elif cell == OBSTABLE:
                grid.add((row, col))

    return initial_row, initial_col, row_size, col_size, grid


def round(
    grid: Grid,
    current_row: int,
    current_col: int,
    dir_row: int,
    dir_col: int,
    row_size: int,
    col_size: int,
) -> Tuple[State, bool]:
    """Do a guard round around the grid"""
    visited: State = set()

    while (current_row, current_col, dir_row, dir_col) not in visited:
        visited.add((current_row, current_col, dir_row, dir_col))

        next_row = current_row + dir_row
        next_col = current_col + dir_col
        if not (0 <= next_row < row_size and 0 <= next_col < col_size):
            return visited, False

        if (next_row, next_col) not in grid:
            # if grid[next_row][next_col] == SPACE:
            current_row = next_row
            current_col = next_col
        else:
            # rotation 90 degrees right
            dir_row, dir_col = dir_col, -dir_row

    return visited, True


def solve(
    initial_row: int, initial_col: int, row_size: int, col_size: int, grid: Grid
) -> int:
    current_row: int = initial_row
    current_col: int = initial_col
    dir_row, dir_col = INITIAL_DIRECTION

    # initial guard round
    visited, is_looped = round(
        grid, current_row, current_col, dir_row, dir_col, row_size, col_size
    )

    # form a set of unique locations
    guard_path: Set[Tuple[int, int]] = {(row, col) for (row, col, _, _) in visited}
    guard_path.remove((initial_row, initial_col))

    total = 0
    for row, col in guard_path:
        grid.add((row, col))

        _, is_looped = round(
            grid, current_row, current_col, dir_row, dir_col, row_size, col_size
        )
        if is_looped:
            total += 1

        grid.remove((row, col))

    return total


def solution(filename: str) -> int:
    initial_row, initial_col, row_size, col_size, grid = parse(filename)
    return solve(initial_row, initial_col, row_size, col_size, grid)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 6
    print(solution("./input.txt"))  # 1575
