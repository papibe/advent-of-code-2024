import re
from typing import List, Tuple


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    numbers: List[int] = []
    for line in data:
        numbers.append(int(line))

    # print(numbers)

    return numbers

def pseudo_random(n: int) -> int:
    def round(n: int):
        n = (n ^ (n * 64)) % 16777216
        n = (n ^ (n // 32)) % 16777216
        n = (n ^ (n * 2048)) % 16777216
        return n

    for _ in range(2000):
        n = round(n)
    return n


def solve(numbers: str) -> int:
    total_sum: int = 0

    for number in numbers:
        total_sum += pseudo_random(number)

    return total_sum


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 37327623
    print(solution("./input.txt"))  # 21147129593
