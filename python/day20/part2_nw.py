import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


START: str = "S"
END: str = "E"
WALL: str = "#"
SPACE: str = "."

import sys

sys.setrecursionlimit(5000) # Set the new recursion limit


def parse(filename: str) -> Tuple[List[str], int, int, int, int]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()


    grid = []
    for line in data:
        grid.append([char for char in line])

    # print(grid)

    start_row: int
    start_col: int
    end_row: int
    end_col: int

    # find start and end
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == START:
                start_row = row
                start_col = col
            elif cell == END:
                end_row = row
                end_col = col

    return grid, start_row, start_col, end_row, end_col

def run(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int
) -> int:
    # BFS setup
    queue: Deque[Tuple[int, int, int, int, int]] = deque(
        [(start_row, start_col, 0)]
    )
    visited = set([(start_row, start_col)])

    # BFS
    while queue:
        row, col, cost = queue.popleft()

        if row == end_row and col == end_col:
            return cost

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[new_row][new_col] == WALL:
                    continue

                if (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, cost + 1))
                    visited.add((new_row, new_col))
    return -1

def solve(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int, required_saves: int
) -> int:
    # main_result = run(grid, start_row, start_col, end_row, end_col)
    main_result = 1417

    queue: Deque[Tuple[int, int, int, int, int]] = deque(
        [(start_row, start_col, 0, 20)]
    )
    visited = set([(start_row, start_col)])
    visited_walls = set()

    # BFS
    while queue:
        row, col, steps, cheats = queue.popleft()

        if main_result - steps < required_saves:
            continue

        if row == end_row and col == end_col:
            print(steps)
            # return steps

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[new_row][new_col] != WALL:

                    if (new_row, new_col) not in visited:
                        queue.append((new_row, new_col, steps + 1, cheats))
                        visited.add((new_row, new_col))

                elif grid[new_row][new_col] == WALL:
                    if cheats > 0:
                        if (new_row, new_col) not in visited_walls:

                            visited_walls.add((new_row, new_col))
                            queue.append((new_row, new_col, steps + 1, cheats - 1))
                            visited_walls.remove((new_row, new_col))
    return -1



    memo = {}

    def dfs(row, col, steps, cheats):
        print(len(memo), steps)
        if row == end_row and col == end_col:
            return steps

        key = (row, col, steps, cheats)
        if key in memo:
            return memo[key]

        cheat_ways = 0

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[new_row][new_col] != WALL:

                    if (new_row, new_col) not in visited:
                        visited.add((new_row, new_col))
                        result = dfs(new_row, new_col, steps + 1, cheats)
                        if main_result - result >= required_saves:
                            cheat_ways += 1
                        visited.remove((new_row, new_col))

                elif grid[new_row][new_col] == WALL:
                    if cheats > 0:
                        if (new_row, new_col) not in visited_walls:

                            visited_walls.add((new_row, new_col))
                            result = dfs(new_row, new_col, steps + 1, cheats - 1)
                            if main_result - result >= required_saves:
                                cheat_ways += 1
                            visited_walls.remove((new_row, new_col))

        memo[key] = cheat_ways
        return cheat_ways


    visited = set([(start_row, start_col)])
    visited_walls = set()
    r = dfs(start_row, start_col, 0, 1)

    return r
    # return len([result for result in results if result >= 100])



def solution(filename: str, required_saves: int) -> int:
    grid, start_row, start_col, end_row, end_col = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col,required_saves)


if __name__ == "__main__":
    print(solution("./example.txt", 50))  # 0
    # print(solution("./input.txt", 100))  # 0
