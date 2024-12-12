from typing import Dict, List, Tuple


def parse(filename: str) -> List[int]:
    with open(filename, "r") as fp:
        data: str = fp.read().strip()

    return [int(n) for n in data.split()]


memo: Dict[Tuple[int, int], int] = {}


def blink(stone: int, reminding: int) -> int:
    if reminding == 0:
        return 1

    key: Tuple[int, int] = (stone, reminding)
    if key in memo:
        return memo[key]

    result: int

    if stone == 0:
        result = blink(1, reminding - 1)

    elif len(str(stone)) % 2 == 0:
        str_stone: str = str(stone)
        first: str = str_stone[: len(str_stone) // 2]
        second: str = str_stone[len(str_stone) // 2 :]
        result = blink(int(first), reminding - 1) + blink(int(second), reminding - 1)

    else:
        result = blink(stone * 2024, reminding - 1)

    memo[key] = result
    return result


def solve(stones: List[int]) -> int:

    size = 0
    for stone in stones:
        size += blink(stone, 75)

    return size


def solution(filename: str) -> int:
    data: List[int] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    # print(solution("./example.txt"))  # 0
    # print(solution("./example2.txt"))  # 0
    print(solution("./input.txt"))  # 0
