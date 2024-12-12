from typing import List, Tuple


def parse(filename: str) -> List[int]:
    with open(filename, "r") as fp:
        data: str = fp.read().strip()

    return [int(n) for n in data.split()]


def blink(stones: List[int]) -> List[int]:
    new_stones: List[int] = []

    for stone in stones:
        if stone == 0:
            new_stones.append(1)

        elif len(str(stone)) % 2 == 0:
            str_stone = str(stone)
            first = str_stone[: len(str_stone) // 2]
            second = str_stone[len(str_stone) // 2 :]
            new_stones.append(int(first))
            new_stones.append(int(second))

        else:
            new_stones.append(stone * 2024)

    return new_stones


def solve(stones: List[int], n_blinks: int) -> Tuple[List[int], int]:
    for _ in range(n_blinks):
        stones = blink(stones)

    return stones, len(stones)


def solution(filename: str, n_blinks: int) -> int:
    stones: List[int] = parse(filename)
    _, result = solve(stones, n_blinks)
    return result


if __name__ == "__main__":
    print(solution("./input.txt", 25))  # 233050
