from typing import List, Tuple

STEPS: List[Tuple[int, int]] = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
]


PATTERNS: List[List[List[str]]] = [
    [
        ["M", ".", "S"],
        [".", "A", "."],
        ["M", ".", "S"],
    ],
    [
        ["M", ".", "M"],
        [".", "A", "."],
        ["S", ".", "S"],
    ],
    [
        ["S", ".", "S"],
        [".", "A", "."],
        ["M", ".", "M"],
    ],
    [
        ["S", ".", "M"],
        [".", "A", "."],
        ["S", ".", "M"],
    ],
]


def check(
    puzzle: List[str], start_row: int, start_col: int, pattern: List[List[str]]
) -> bool:
    """check if the puzzle matches a pattern at (start_row, start_col)"""

    for row, line in enumerate(pattern):
        for col, char in enumerate(line):
            if char == ".":
                continue
            data_row: int = start_row + row
            data_col: int = start_col + col
            if not (0 <= data_row < len(puzzle) and 0 <= data_col < len(puzzle[0])):
                return False

            if char != puzzle[data_row][data_col]:
                return False

    return True


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()
    return data


def solve(data: List[str]) -> int:
    total: int = 0

    for row, line in enumerate(data):
        for col, item in enumerate(line):
            for pattern in PATTERNS:
                if check(data, row, col, pattern):
                    total += 1

    return total


def solution(filename: str) -> int:
    data: List[str] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 9
    print(solution("./input.txt"))  # 1835
