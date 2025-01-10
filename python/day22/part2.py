from typing import Dict, List, Tuple


def parse(filename: str) -> List[int]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    numbers: List[int] = []
    for line in data:
        numbers.append(int(line))

    return numbers


def pseudo_random(n: int) -> int:
    n = (n ^ (n * 64)) % 16777216
    n = (n ^ (n // 32)) % 16777216
    n = (n ^ (n * 2048)) % 16777216
    return n


def solve(numbers: List[int]) -> int:
    buyers: List[List[int]] = []
    for number in numbers:
        n = pseudo_random(number)
        single_buyer = [n]
        for _ in range(2000):
            n = pseudo_random(n)
            single_buyer.append(n % 10)

        buyers.append(single_buyer)

    best: Dict[Tuple[int, int, int, int], int] = {}
    for b in buyers:
        seen = set()
        for i in range(len(b) - 4):
            d1, d2, d3, d4, d5 = b[i], b[i + 1], b[i + 2], b[i + 3], b[i + 4]
            diff_key = (d2 - d1, d3 - d2, d4 - d3, d5 - d4)
            if diff_key in seen:
                continue
            seen.add(diff_key)
            best[diff_key] = best.get(diff_key, 0) + d5

    return max(best.values())


def solution(filename: str) -> int:
    data: List[int] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 23
    print(solution("./input.txt"))  # 2445
