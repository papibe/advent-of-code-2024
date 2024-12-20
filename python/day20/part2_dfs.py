import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


START: str = "S"
END: str = "E"
WALL: str = "#"
SPACE: str = "."

NOT_USING_CHEATS: int = 0
USING_CHEATS: int = 1
ALREADY_USED_CHEATS: int = 2

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
    main_result = run(grid, start_row, start_col, end_row, end_col)
    print(f"{main_result = }")
    # main_result = 1417
    # main_result = 84


    memo = {}

    def dfs(row, col, steps, cheats, use_cheats):
        print(len(memo), steps)
        if row == end_row and col == end_col:
            print(f"{steps =}")
            return steps

        if steps > main_result:
            return main_result

        key = (row, col, steps, cheats, use_cheats)
        if key in memo:
            print("save!")
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

                    if (new_row, new_col, cheats, use_cheats) not in visited:

                        if use_cheats == USING_CHEATS:
                            use_cheats = ALREADY_USED_CHEATS
                            # result = run(grid, new_row, new_col, end_row, end_col)
                        # else:
                            visited.add((new_row, new_col, cheats, use_cheats))
                            result = dfs(new_row, new_col, steps + 1, cheats, use_cheats)
                            visited.remove((new_row, new_col, cheats, use_cheats))

                            if main_result - result >= required_saves:
                                cheat_ways += 1


                elif grid[new_row][new_col] == WALL:
                    if use_cheats != ALREADY_USED_CHEATS and cheats > 0:
                        if (new_row, new_col, cheats, use_cheats) not in visited:
                            print("using cheats")
                            use_cheats = USING_CHEATS
                            visited.add((new_row, new_col, cheats, use_cheats))
                            result = dfs(new_row, new_col, steps + 1, cheats - 1, use_cheats)
                            if main_result - result >= required_saves:
                                cheat_ways += 1
                            visited.remove((new_row, new_col, cheats, use_cheats))

        memo[key] = cheat_ways
        return cheat_ways


    visited = set([(start_row, start_col, 0, 0)])
    # visited_walls = set()
    r = dfs(start_row, start_col, 0, 1, NOT_USING_CHEATS)

    return r
    # return len([result for result in results if result >= 100])



def solution(filename: str, required_saves: int) -> int:
    grid, start_row, start_col, end_row, end_col = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col,required_saves)


if __name__ == "__main__":
    print(solution("./example.txt", 20))  # 0
    # print(solution("./input.txt", 100))  # 0
