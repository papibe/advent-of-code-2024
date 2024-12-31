from collections import deque, namedtuple
from typing import Deque, List, Set, Tuple

Byte = namedtuple("Byte", ["x", "y"])


def parse(filename: str, fallen: int) -> Tuple[Set[Byte], List[Byte]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    fbytes: Set[Byte] = set()
    for index in range(fallen):
        line: str = data[index]
        numbers: List[str] = line.split(",")
        fbytes.add(Byte(int(numbers[0]), int(numbers[1])))

    rbytes: List[Byte] = []
    for index in range(fallen, len(data)):
        line = data[index]
        numbers = line.split(",")
        rbytes.append(Byte(int(numbers[0]), int(numbers[1])))

    return fbytes, rbytes


def run(fbytes: Set[Byte], rbytes: List[Byte], index: int, size: int) -> int:
    # BFS set up
    row: int = 0
    col: int = 0
    queue: Deque[Tuple[int, int, int]] = deque([(row, col, 0)])
    visited: Set[Tuple[int, int]] = set([(row, col)])

    # new walls
    fallen_bytes: Set[Byte] = set()
    for i in range(index + 1):
        fallen_bytes.add(rbytes[i])

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

                if (new_row, new_col) in fbytes or (new_row, new_col) in fallen_bytes:
                    continue

                queue.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))

    return -1


def solve(fbytes: Set[Byte], rbytes: List[Byte], size: int) -> str:
    lower: int = 0
    upper: int = len(rbytes) - 1
    while lower < upper:
        middle: int = (lower + upper) // 2
        result: int = run(fbytes, rbytes, middle, size)

        if result == -1:
            upper = middle
        else:
            lower = middle + 1

    rbyte: Byte = rbytes[lower]
    return f"{rbyte.x},{rbyte.y}"


def solution(filename: str, size: int, fallen: int) -> str:
    fbytes, rbytes = parse(filename, fallen)
    return solve(fbytes, rbytes, size)


if __name__ == "__main__":
    print(solution("./example.txt", 6, 12))  # 6,1
    print(solution("./input.txt", 70, 1024))  # 16,44
