from typing import List, Set, Tuple

Grid = List[List[str]]
State = Set[Tuple[int, int, int, int]]

INITIAL_DIRECTION: Tuple[int, int] = (-1, 0)
SPACE: str = "."
GUARD: str = "^"
OBSTABLE: str = "#"


def parse(filename: str) -> Tuple[int, int, Grid]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    # build grid and get guard initial position
    grid: Grid = []
    initial_row: int
    initial_col: int

    for row, line in enumerate(data):
        new_row: List[str] = []
        for col, cell in enumerate(line):
            # record initial position and replce it with space
            if cell == GUARD:
                initial_row = row
                initial_col = col
                new_row.append(SPACE)
            else:
                new_row.append(cell)
        grid.append(new_row)

    return initial_row, initial_col, grid


def round(
    grid: Grid, current_row: int, current_col: int, dir_row: int, dir_col: int
) -> Tuple[State, bool]:
    """Do a guard round around the grid"""
    visited: State = set()

    while (current_row, current_col, dir_row, dir_col) not in visited:
        visited.add((current_row, current_col, dir_row, dir_col))

        next_row = current_row + dir_row
        next_col = current_col + dir_col
        if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
            return visited, False

        if grid[next_row][next_col] == SPACE:
            current_row = next_row
            current_col = next_col
        else:
            # rotation 90 degrees right
            dir_row, dir_col = dir_col, -dir_row

    return visited, True


def solve(initial_row: int, initial_col: int, grid: Grid) -> int:
    current_row: int = initial_row
    current_col: int = initial_col
    dir_row, dir_col = INITIAL_DIRECTION

    # initial guard round
    visited, is_looped = round(grid, current_row, current_col, dir_row, dir_col)

    # form a set of unique locations
    guard_path: Set[Tuple[int, int]] = {(row, col) for (row, col, _, _) in visited}
    guard_path.remove((initial_row, initial_col))

    total = 0
    for row, col in guard_path:
        grid[row][col] = OBSTABLE

        _, is_looped = round(grid, current_row, current_col, dir_row, dir_col)
        if is_looped:
            total += 1

        grid[row][col] = SPACE

    return total


def solution(filename: str) -> int:
    initial_row, initial_col, grid = parse(filename)
    return solve(initial_row, initial_col, grid)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 6
    print(solution("./input.txt"))  # 1575
