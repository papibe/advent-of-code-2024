from typing import List, Tuple

Grid = List[List[str]]

INITIAL_DIRECTION: Tuple[int, int] = (-1, 0)
SPACE: str = "."
GUARD: str = "^"


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


def solve(initial_row: int, initial_col: int, grid: Grid) -> int:
    current_row: int = initial_row
    current_col: int = initial_col
    dir_row, dir_col = INITIAL_DIRECTION

    visited = set([(current_row, current_col)])

    while True:

        next_row = current_row + dir_row
        next_col = current_col + dir_col
        if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
            return len(visited)

        if grid[next_row][next_col] == SPACE:
            current_row = next_row
            current_col = next_col
        else:
            # rotation 90 degrees right
            dir_row, dir_col = dir_col, -dir_row

        visited.add((current_row, current_col))


def solution(filename: str) -> int:
    initial_row, initial_col, grid = parse(filename)
    return solve(initial_row, initial_col, grid)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 41
    print(solution("./input.txt"))  # 4656
