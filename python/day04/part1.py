from typing import List

STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()
    return data


def solve(puzzle: List[str]) -> int:
    total: int = 0

    for row, line in enumerate(puzzle):
        for col, _ in enumerate(line):

            # go all directions
            for dir_row, dir_col in STEPS:
                new_row: int = row
                new_col: int = col

                # when chose a direction check if matches the word
                for char in "XMAS":
                    if (
                        0 <= new_row < len(puzzle)
                        and 0 <= new_col < len(puzzle[0])
                        and char == puzzle[new_row][new_col]
                    ):
                        new_row += dir_row
                        new_col += dir_col
                    else:
                        break
                else:
                    total += 1

    return total


def solution(filename: str) -> int:
    puzzle: List[str] = parse(filename)
    return solve(puzzle)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 18
    print(solution("./input.txt"))  # 2434
