from typing import List, Tuple


class Dir:
    UP: str = "^"
    DOWN: str = "v"
    LEFT: str = "<"
    RIGHT: str = ">"


class Grid:
    ROBOT: str = "@"
    SPACE: str = "."
    WALL: str = "#"
    BOX: str = "O"


Warehouse = List[List[str]]
Movements = str


def parse(filename: str) -> Tuple[Warehouse, Movements, int, int]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    warehouse: Warehouse = []
    for line in blocks[0].splitlines():
        warehouse.append([char for char in line])

    # get robot position:
    for row, row_line in enumerate(warehouse):
        for col, cell in enumerate(row_line):
            if cell == Grid.ROBOT:
                break
        else:
            continue
        break

    # patch position of robot
    warehouse[row][col] = Grid.SPACE

    # join movement lines
    movements: List[str] = []
    for line in blocks[1].splitlines():
        movements.append(line)

    return warehouse, "".join(movements), row, col


def makemove(
    warehouse: Warehouse, row: int, col: int, row_dir: int, col_dir: int
) -> Tuple[int, int]:
    """Execute the actual movement on the grid. Including pusing boxes"""
    next_row: int = row + row_dir
    next_col: int = col + col_dir

    if warehouse[next_row][next_col] == Grid.SPACE:
        return next_row, next_col

    if warehouse[next_row][next_col] == Grid.WALL:
        return row, col

    # next postition is a box. Finding a space
    current_row: int = next_row
    current_col: int = next_col
    while warehouse[current_row][current_col] not in [Grid.SPACE, Grid.WALL]:
        current_row += row_dir
        current_col += col_dir

    if warehouse[current_row][current_col] == "#":
        return row, col

    # space behind a box
    while not (current_row == next_row and current_col == next_col):
        previous_row: int = current_row - row_dir
        previous_col: int = current_col - col_dir

        # swap
        warehouse[current_row][current_col], warehouse[previous_row][previous_col] = (
            warehouse[previous_row][previous_col],
            warehouse[current_row][current_col],
        )

        current_row = previous_row
        current_col = previous_col

    return current_row, current_col


def solve(warehouse: Warehouse, movements: Movements, row: int, col: int) -> int:
    # run movements
    for move in movements:
        match move:
            case Dir.LEFT:
                row, col = makemove(warehouse, row, col, 0, -1)
            case Dir.RIGHT:
                row, col = makemove(warehouse, row, col, 0, 1)
            case Dir.UP:
                row, col = makemove(warehouse, row, col, -1, 0)
            case Dir.DOWN:
                row, col = makemove(warehouse, row, col, 1, 0)
            case _:
                raise RuntimeError(f"Direction not recognized: {move}")

    # calculate the sum of the GPS coordinates
    coordinates_sum: int = 0
    for row, line in enumerate(warehouse):
        for c, cell in enumerate(line):
            if cell == Grid.BOX:
                coordinates_sum += 100 * row + c

    return coordinates_sum


def solution(filename: str) -> int:
    warehouse, movements, robot_row, robot_col = parse(filename)
    return solve(warehouse, movements, robot_row, robot_col)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 2028
    print(solution("./example2.txt"))  # 10092
    print(solution("./input.txt"))  # 1463715
