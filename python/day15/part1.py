import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    warehouse = []
    for line in blocks[0].splitlines():
        warehouse.append([char for char in line])

    movements = []
    for line in blocks[1].splitlines():
        movements.append(line)

    # print(warehouse)
    # print("".join(movements))

    return warehouse, "".join(movements)

def makemove(warehouse, row, col, row_dir, col_dir) -> Tuple[int, int]:
    next_row = row + row_dir
    next_col = col + col_dir

    print(f"{next_row = }, {next_col = }")

    if warehouse[next_row][next_col] == ".":
        return next_row, next_col

    if warehouse[next_row][next_col] == "#":
        return row, col

    # next is a box
    # find a space
    current_row = next_row
    current_col = next_col
    while warehouse[current_row][current_col] not in [".", "#"]:
        current_row += row_dir
        current_col += col_dir

    if warehouse[current_row][current_col] == "#":
        return row, col

    # print(current_row, current_col, warehouse[current_row][current_col])

    # space behind a box
    while not (current_row == next_row and current_col == next_col):
        # print(current_row, current_col)
        previous_row = current_row - row_dir
        previous_col = current_col - col_dir
        warehouse[current_row][current_col], warehouse[previous_row][previous_col] = warehouse[previous_row][previous_col], warehouse[current_row][current_col]

        # print("++++++++++")
        # for r, line in enumerate(warehouse):
        #     for c, cell in enumerate(line):
        #         if r == row and c == col:
        #             print("@", end="")
        #         else:
        #             print(warehouse[r][c], end="")
        #     print()
        # print("-------------")

        current_row = previous_row
        current_col = previous_col



    return current_row, current_col


    return row, col

def solve(warehouse, movements) -> int:
    # get robot position:
    for row, line in enumerate(warehouse):
        for col, cell in enumerate(line):
            if cell == "@":
                break
        else:
            continue
        break

    # patch position of robot
    warehouse[row][col] = "."

    # run movements
    for move in movements:
        print(move)
        if move == "<":
            row, col = makemove(warehouse, row, col, 0, -1)
        elif move == ">":
            row, col = makemove(warehouse, row, col, 0, 1)
        elif move == "^":
            row, col = makemove(warehouse, row, col, -1, 0)
        elif move == "v":
            row, col = makemove(warehouse, row, col, 1, 0)
        else:
            raise Exception("bla")

        # for r, line in enumerate(warehouse):
        #     for c, cell in enumerate(line):
        #         if r == row and c == col:
        #             print("@", end="")
        #         else:
        #             print(warehouse[r][c], end="")
        #     print()
        # print()

    total = 0
    for r, line in enumerate(warehouse):
        for c, cell in enumerate(line):
            if cell == "O":
                total += 100 * r + c
    return total


def solution(filename: str) -> int:
    warehouse, movements = parse(filename)
    return solve(warehouse, movements)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 0
    print(solution("./example2.txt"))  # 0
    print(solution("./input.txt"))  # 0
