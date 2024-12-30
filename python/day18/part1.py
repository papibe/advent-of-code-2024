from collections import deque, namedtuple
from typing import Deque, List, Set, Tuple

Byte = namedtuple("Byte", ["x", "y"])


def parse(filename: str, fallen: int) -> Tuple[Set[Byte], Set[Byte]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    fbytes: Set[Byte] = set()
    for index, line in enumerate(data):
        if index >= fallen:
            break
        numbers = line.split(",")
        fbytes.add(Byte(int(numbers[0]), int(numbers[1])))

    rbytes: Set[Byte] = set()
    for index, line in enumerate(data):
        if index < fallen:
            continue
        numbers = line.split(",")
        rbytes.add(Byte(int(numbers[0]), int(numbers[1])))

    return fbytes, rbytes


def solve(fbytes: Set[Byte], rbytes: Set[Byte], size: int) -> int:
    # BFS set up
    row: int = 0
    col: int = 0
    queue: Deque[Tuple[int, int, int]] = deque([(row, col, 0)])
    visited: Set[Tuple[int, int]] = set([(row, col)])

    # BFS
    while queue:
        row, col, steps = queue.popleft()

        if row == size and col == size:
            return steps

        for new_row, new_col in [
            (row, col + 1),
            (row, col - 1),
            (row + 1, col),
            (row - 1, col),
        ]:
            if 0 <= new_row <= size and 0 <= new_col <= size:

                if (new_row, new_col) in visited:
                    continue

                if (new_row, new_col) in fbytes:
                    continue

                queue.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))

    return -1


def solution(filename: str, size: int, fallen: int) -> int:
    fbytes, rbytes = parse(filename, fallen)
    return solve(fbytes, rbytes, size)


if __name__ == "__main__":
    print(solution("./example.txt", 6, 12))  # 0
    print(solution("./input.txt", 70, 1024))  # 0
