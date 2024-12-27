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

    # for _ in range(2000):
    #     n = round(n)
    return round(n)


def solve(numbers: str) -> int:
    sn = []

    buyers = []
    for number in numbers:
        n = pseudo_random(number)
        single_buyer = [n]
        for _ in range(2000):
            n = pseudo_random(n)
            single_buyer.append(n % 10)

        buyers.append(single_buyer)

    best = {}
    total = 0
    for b in buyers:
        seen = set()
        for i in range(len(b) - 4):
            d1, d2, d3, d4, d5 = b[i],b[i+1],b[i+2],b[i+3], b[i+4]
            diff_key = (d2 - d1, d3 - d2, d4 - d3, d5 - d4)
            if diff_key in seen:
                continue
            seen.add(diff_key)
            best[diff_key] = best.get(diff_key, 0) + d5

    # print(best)

    return max(best.values())


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 23
    print(solution("./input.txt"))  # 2445
