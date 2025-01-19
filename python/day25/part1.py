from typing import List, Tuple

Lock = List[str]
Key = List[str]
Height = List[int]


def parse(filename: str) -> Tuple[List[Lock], List[Key]]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    locks: List[Lock] = []
    keys: List[Key] = []

    for block in blocks:
        if block[0] == "#":
            locks.append(block.splitlines())
        elif block[0] == ".":
            keys.append(block.splitlines())
        else:
            raise RuntimeError("invalid format")

    return locks, keys


def solve(locks: List[Lock], keys: List[Key]) -> int:
    # get lock heights
    lock_heights: List[Height] = []
    for lock in locks:
        lock_height = [-1] * len(lock[0])
        for col in range(len(lock[0])):
            for row in range(len(lock)):
                if lock[row][col] == "#":
                    lock_height[col] += 1

        lock_heights.append(lock_height)

    # get pin heights
    key_heights: List[Height] = []
    for key in keys:
        key_height = [-1] * len(key[0])
        for col in range(len(key[0])):
            for row in range(len(key)):
                if key[row][col] == "#":
                    key_height[col] += 1

        key_heights.append(key_height)

    # count overall keys and locks fits
    key_lock_fits: int = 0
    for key_height in key_heights:
        for lock_height in lock_heights:
            for col in range(5):
                key_pin = key_height[col]
                lock_pin = lock_height[col]
                if key_pin + lock_pin > 5:
                    break
            else:
                key_lock_fits += 1

    return key_lock_fits


def solution(filename: str) -> int:
    locks, keys = parse(filename)
    return solve(locks, keys)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 3
    print(solution("./input.txt"))  # 3127
