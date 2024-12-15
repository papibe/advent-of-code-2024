import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    warehouse = []
    for line in blocks[0].splitlines():
        wrow = []
        for char in line:
            if char == "#":
                wrow.append("#")
                wrow.append("#")
            elif char == "O":
                wrow.append("[")
                wrow.append("]")
            elif char == ".":
                wrow.append(".")
                wrow.append(".")
            elif char == "@":
                wrow.append("@")
                wrow.append(".")

        warehouse.append(wrow)

    movements = []
    for line in blocks[1].splitlines():
        movements.append(line)


    for r, line in enumerate(warehouse):
        print("".join(line))
    print()

    # print("".join(movements))

    return warehouse, "".join(movements)


def spacialmove(warehouse, row, col, row_dir, col_dir) -> Tuple[int, int]:
    next_row = row + row_dir
    next_col = col + col_dir

    if warehouse[next_row][next_col] == ".":
        return next_row, next_col

    if warehouse[next_row][next_col] == "#":
        return row, col

    # # BFS init
    # queue = deque([(next_row, next_col)])
    # affected = set([(next_row, next_col)])

    queue = deque([(row, col)])
    affected = set([(row, col)])


    # BFS
    while queue:
        current_row, current_col = queue.popleft()

        next_row = current_row + row_dir
        next_col = current_col + col_dir

        if warehouse[next_row][next_col] == "#":
            return row, col

        if warehouse[next_row][next_col] == "]":
            assert warehouse[next_row ][next_col - 1] == "["

            queue.append((next_row, next_col))
            queue.append((next_row, next_col - 1))

            affected.add((next_row, next_col))
            affected.add((next_row, next_col - 1))

        elif warehouse[next_row][next_col] == "[":
            assert warehouse[next_row][next_col + 1] == "]"

            queue.append((next_row, next_col))
            queue.append((next_row, next_col + 1))

            affected.add((next_row, next_col))
            affected.add((next_row, next_col + 1))



    print(affected)

    while affected:
        for r, c in sorted(affected):
            nr = r + row_dir
            nc = c + col_dir

            if (nr, nc) not in affected:
                # move
                assert warehouse[nr][nc] == "."
                warehouse[nr][nc] = warehouse[r][c]
                warehouse[r][c] = "."
                affected.remove((r, c))

    return row + row_dir, col + col_dir


def makemove(warehouse, row, col, row_dir, col_dir) -> Tuple[int, int]:

    if row_dir != 0:
        return spacialmove(warehouse, row, col, row_dir, col_dir)

    next_row = row + row_dir
    next_col = col + col_dir

    # print(f"{next_row = }, {next_col = }")

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
            if cell == "[":
                total += 100 * r + c
    return total


def solution(filename: str) -> int:
    warehouse, movements = parse(filename)
    return solve(warehouse, movements)


if __name__ == "__main__":
    # print(solution("./example1.txt"))  # 0
    # print(solution("./example2.txt"))  # 0
    # print(solution("./example3.txt"))  # 0
    print(solution("./input.txt"))  # 1481392
