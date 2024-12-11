import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    map_ = []
    for line in data:
        row = [int(char) for char in line]
        map_.append(row)

    # print(map_)

    return map_


def solve(data: List[str]) -> int:
    # get trailheads:
    trailheads = []
    for row, line in enumerate(data):
        for col, trail in enumerate(line):
            if trail == 0:
                trailheads.append((row, col))

    score: int = 0
    for trailhead in trailheads:
        # BFS init
        queue = deque([trailhead])
        visited = set()
        visited.add(trailhead)

        while queue:
            trailhead = queue.popleft()
            slope = data[trailhead[0]][trailhead[1]]
            if slope == 9:
                score += 1
                continue

            for step_row, step_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row = trailhead[0] + step_row
                new_col = trailhead[1] + step_col

                if 0 <= new_row < len(data) and 0 <= new_col < len(data[0]):
                    new_slope = data[new_row][new_col]
                    if new_slope == slope + 1 and (new_row, new_col) not in visited:
                        queue.append((new_row, new_col))
                        visited.add((new_row, new_col))


    return score


def solution(filename: str) -> int:
    data: List[str] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 0
    print(solution("./input.txt"))  # 0
