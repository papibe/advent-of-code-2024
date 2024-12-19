from typing import Dict, List, Tuple


def parse(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    towels: List[str] = [towel.strip() for towel in blocks[0].split(",")]
    patterns: List[str] = blocks[1].splitlines()

    return towels, patterns


def possible_ways(pattern: str, towels: List[str]) -> int:
    memo: Dict[Tuple[str, int], int] = {}

    def dfs(pattern: str, index: int) -> int:
        if index > len(pattern):
            return 0

        if index == len(pattern):
            return 1

        if (pattern, index) in memo:
            return memo[(pattern, index)]

        ways: int = 0
        for towel in towels:
            if pattern[index:].startswith(towel):
                ways += dfs(pattern, index + len(towel))

        memo[(pattern, index)] = ways
        return ways

    return dfs(pattern, 0)


def solve(towels: List[str], patterns: List[str]) -> int:
    total_ways: int = 0

    for pattern in patterns:
        total_ways += possible_ways(pattern, towels)

    return total_ways


def solution(filename: str) -> int:
    towels, patterns = parse(filename)
    return solve(towels, patterns)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 16
    print(solution("./input.txt"))  # 752461716635602
