from typing import List, Tuple


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
    # sort both locations
    left_locations.sort()
    right_locations.sort()

    # calculate distances
    total_distance: int = 0
    for left, right in zip(left_locations, right_locations):
        total_distance += abs(right - left)

    return total_distance


def solution(filename: str) -> int:
    left_locations, right_locations = parse(filename)
    return solve(left_locations, right_locations)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 11
    print(solution("./input.txt"))  # 2192892
