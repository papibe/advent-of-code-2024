from typing import Dict, List, Tuple


def parse(filename: str) -> Tuple[List[int], List[int]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    left_locations: List[int] = []
    right_locations: List[int] = []

    for line in data:
        numbers = line.split()
        left_locations.append(int(numbers[0]))
        right_locations.append(int(numbers[1]))

    return left_locations, right_locations


def solve(left_locations: List[int], right_locations: List[int]) -> int:
    # calculate right side frequencies
    frequencies: Dict[int, int] = {}
    for r in right_locations:
        frequencies[r] = frequencies.get(r, 0) + 1

    # calculate score
    score = 0
    for left in left_locations:
        if left in frequencies:
            score += left * frequencies[left]

    return score


def solution(filename: str) -> int:
    left_locations, right_locations = parse(filename)
    return solve(left_locations, right_locations)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 31
    print(solution("./input.txt"))  # 22962826
