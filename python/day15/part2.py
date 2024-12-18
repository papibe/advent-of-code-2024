from collections import deque
from typing import Deque, List, Tuple


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
    BIG_BOX_LEFT: str = "["
    BIG_BOX_RIGHT: str = "]"


Warehouse = List[List[str]]
Movements = str


def parse(filename: str) -> Tuple[Warehouse, Movements, int, int]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    warehouse: Warehouse = []
    for line in blocks[0].splitlines():
        warehouse_row: List[str] = []
        for char in line:
            if char == Grid.WALL:
                warehouse_row.append(Grid.WALL)
                warehouse_row.append(Grid.WALL)
            elif char == Grid.BOX:
                warehouse_row.append(Grid.BIG_BOX_LEFT)
                warehouse_row.append(Grid.BIG_BOX_RIGHT)
            elif char == Grid.SPACE:
                warehouse_row.append(Grid.SPACE)
                warehouse_row.append(Grid.SPACE)
            elif char == Grid.ROBOT:
                warehouse_row.append(Grid.ROBOT)
                warehouse_row.append(Grid.SPACE)

        warehouse.append(warehouse_row)

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

    movements: List[str] = []
    for line in blocks[1].splitlines():
        movements.append(line)

    return warehouse, "".join(movements), row, col


def spacialmove(
    warehouse: Warehouse, row: int, col: int, row_dir: int, col_dir: int
) -> Tuple[int, int]:
    """Move up and down and push potentially a buch of boxes"""
    next_row: int = row + row_dir
    next_col: int = col + col_dir

    if warehouse[next_row][next_col] == Grid.SPACE:
        return next_row, next_col

    if warehouse[next_row][next_col] == Grid.WALL:
        return row, col

    # BFS init
    queue: Deque[Tuple[int, int]] = deque([(row, col)])
    affected = set([(row, col)])

    # BFS
    while queue:
        current_row, current_col = queue.popleft()

        next_row = current_row + row_dir
        next_col = current_col + col_dir

        if warehouse[next_row][next_col] == Grid.WALL:
            return row, col

        if warehouse[next_row][next_col] == Grid.BIG_BOX_RIGHT:
            assert warehouse[next_row][next_col - 1] == Grid.BIG_BOX_LEFT

            queue.append((next_row, next_col))
            queue.append((next_row, next_col - 1))

            affected.add((next_row, next_col))
            affected.add((next_row, next_col - 1))

        elif warehouse[next_row][next_col] == Grid.BIG_BOX_LEFT:
            assert warehouse[next_row][next_col + 1] == Grid.BIG_BOX_RIGHT

            queue.append((next_row, next_col))
            queue.append((next_row, next_col + 1))

            affected.add((next_row, next_col))
            affected.add((next_row, next_col + 1))

    while affected:
        for affected_row, affected_col in sorted(affected):
            nr: int = affected_row + row_dir
            nc: int = affected_col + col_dir

            if (nr, nc) not in affected:
                # push and move
                assert warehouse[nr][nc] == Grid.SPACE
                warehouse[nr][nc] = warehouse[affected_row][affected_col]
                warehouse[affected_row][affected_col] = Grid.SPACE
                affected.remove((affected_row, affected_col))

    return row + row_dir, col + col_dir


def makemove(
    warehouse: Warehouse, row: int, col: int, row_dir: int, col_dir: int
) -> Tuple[int, int]:
    """Execute the actual movement on the grid. Including pusing boxes"""

    if row_dir != 0:
        return spacialmove(warehouse, row, col, row_dir, col_dir)

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
            if cell == Grid.BIG_BOX_LEFT:
                coordinates_sum += 100 * row + c

    return coordinates_sum


def solution(filename: str) -> int:
    warehouse, movements, robot_row, robot_col = parse(filename)
    return solve(warehouse, movements, robot_row, robot_col)


if __name__ == "__main__":
    assert solution("./example2.txt") == 9021
    assert solution("./input.txt") == 1481392
    # print(solution("./example2.txt"))  # 9021
    # print(solution("./input.txt"))  # 1481392
