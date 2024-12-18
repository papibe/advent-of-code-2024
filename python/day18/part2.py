import re
from collections import deque, defaultdict, namedtuple
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple

Byte = namedtuple("Byte", ["x", "y"])


def parse(filename: str, fallen) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    fbytes = set()
    for index, line in enumerate(data):
        if index >= fallen:
            break
        numbers = line.split(",")
        fbytes.add(Byte(int(numbers[0]), int(numbers[1])))

    rbytes = deque([])
    for index, line in enumerate(data):
        if index < fallen:
            continue
        numbers = line.split(",")
        rbytes.append(Byte(int(numbers[0]), int(numbers[1])))

    # print(len(fbytes), len(rbytes))

    # print(fbytes)

    return fbytes, rbytes


def fall(fbytes, size):
    new_fbytes = set()
    for fbyte in fbytes:
        if fbyte.y + 1 <= size:
            new_fbytes.add(Byte(fbyte.x, fbyte.y + 1))
    return new_fbytes


def run(fbytes: List[str], rbytes, size: int) -> int:

    row = 0
    col = 0
    queue = deque([(row, col, 0)])
    visited = set([(row, col)])

    # BFS
    while queue:
        row, col, steps = queue.popleft()
        # print(row, col, steps)
        if row == size and col == size:
            return steps



        for new_row, new_col in [(row, col + 1), (row, col - 1), (row + 1, col),(row - 1 , col)]:
            # print(f"{new_row = }, {new_col = }")
            if 0 <= new_row <= size and 0 <= new_col <= size:

                if (new_row, new_col) in visited:
                    continue

                if (new_row, new_col) in fbytes:
                    continue

                queue.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))

    return -1

def solve(fbytes: List[str], rbytes, size: int) -> int:
    while rbytes:
        # print(len(rbytes))
        rbyte = rbytes.popleft()
        fbytes.add(rbyte)

        result = run(fbytes, rbytes, size)
        if result == -1:
            return rbyte



def solution(filename: str, size: int, fallen) -> int:
    fbytes, rbytes = parse(filename, fallen)
    return solve(fbytes, rbytes, size)


if __name__ == "__main__":
    print(solution("./example.txt", 6, 12))  # 0
    print(solution("./input.txt", 70, 1024))  # 0