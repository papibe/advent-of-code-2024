import re
from typing import List, Tuple


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read()

    return data


def solve(data: str) -> int:
    total_sum: int = 0

    re_mul: str = r"mul\((\d+),(\d+)\)"

    matches: List[Tuple[str, str]] = re.findall(re_mul, data, re.DOTALL)
    for m in matches:
        total_sum += int(m[0]) * int(m[1])

    return total_sum


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 161
    print(solution("./input.txt"))  # 188741603
