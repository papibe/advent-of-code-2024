from typing import List, Tuple


def parse(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    towels: List[str] = [towel.strip() for towel in blocks[0].split(",")]
    patterns: List[str] = blocks[1].splitlines()

    return towels, patterns


def is_possible(pattern: str, towels: List[str]) -> bool:

    def dfs(pattern: str, index: int) -> bool:
        if index >= len(pattern):
            return False

        if index == len(pattern) - 1:
            return True

        for towel in towels:
            if pattern[index:].startswith(towel):
                if dfs(pattern, index + len(towel)):
                    return True

        return False

    return dfs(pattern, 0)


def solve(towels: List[str], patterns: List[str]) -> int:
    possible: int = 0

    for pattern in patterns:
        if is_possible(pattern, towels):
            possible += 1

    return possible


def solution(filename: str) -> int:
    towels, patterns = parse(filename)
    return solve(towels, patterns)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 6
    print(solution("./input.txt"))  # 265
