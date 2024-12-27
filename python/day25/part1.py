import re
from collections import deque, defaultdict
from typing import List, Tuple, Dict


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        blocks: str = fp.read().split("\n\n")

    locks = []
    keys = []
    for block in blocks:
        if block[0] == "#":
            locks.append(block.splitlines())
        elif block[0] == ".":
            keys.append(block.splitlines())
        else:
            raise RuntimeError("blah")

    # print(locks)
    # print(keys)

    return locks, keys


def solve(locks, keys) -> int:
    total_sum: int = 0

    lock_pins = []
    for lock in locks:
        lock_pin = [-1] * len(lock[0])
        for col in range(len(lock[0])):
            for row in range(len(lock)):
                if lock[row][col] ==  "#":
                    lock_pin[col] += 1
        
        lock_pins.append(lock_pin)

    key_pins = []
    for key in keys:
        key_pin = [-1] * len(key[0])
        for col in range(len(key[0])):
            for row in range(len(key)):
                if key[row][col] ==  "#":
                    key_pin[col] += 1
        
        key_pins.append(key_pin)


    # print(lock_pins)
    # print()
    # print(key_pins)


    counter = 0
    for key in key_pins:
        for lock in lock_pins:
            for col, pin in enumerate(lock):
                kpin = key[col]
                lpin = lock[col]
                if kpin + lpin > 5:
                    break
            else:
                counter += 1


    return counter


def solution(filename: str) -> int:

    locks, keys = parse(filename)
    return solve(locks, keys)


if __name__ == "__main__":
    print(solution("./example.txt"))  #
    print(solution("./input.txt"))  # 
