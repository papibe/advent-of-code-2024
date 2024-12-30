import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple
import heapq as hq

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
    # dijkstra setup
    distances: List[List[int]] = []
    for _ in range(len(grid)):
        distances.append([float("inf") for _ in range(len(grid[0]))])  # type: ignore


    pqueue = [(0, (start_row, start_col))]
    hq.heapify(pqueue)
    previous = {}
    visited = set([(start_row, start_col)])

    # dijkstra
    while pqueue:
        distance, (row, col) = hq.heappop(pqueue)

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[new_row][new_col] == WALL:
                    continue

                new_distance: int = distance + 1
                if new_distance < distances[new_row][new_col]:
                    distances[new_row][new_col] = new_distance
                    previous[(new_row, new_col)] = (row, col)

                    hq.heappush(pqueue, (new_distance, (new_row, new_col)))
                    visited.add((new_row, new_col))


    path = []
    current =  (end_row, end_col)
    while current != (start_row, start_col):
        path.append(current)
        current = previous[current]
    path.append((start_row, start_col))

    return distances, path

def get_radius(grid, srow, scol, cheats):
   # BFS init
    queue = deque( [(srow, scol, cheats)] )
    visited = set([(srow, scol)])

    # BFS
    while queue:
        row, col, cheats = queue.popleft()

        if cheats <= 0:
            continue

        for new_row, new_col in [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                if (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, cheats - 1))
                    visited.add((new_row, new_col))

    # clean potential cheat destinations
    cheat_desintations = set()
    for (row, col) in visited:
        if grid[row][col] != WALL:
            d = abs(srow - row) + abs(scol - col)
            assert d <= 20
            if d == 0:
                continue
            cheat_desintations.add((row, col))


    return cheat_desintations



def solve(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int, required_saves: int
) -> int:
    d_to_start, path1 = run(grid, start_row, start_col, end_row, end_col)
    d_to_end, path2 = run(grid, end_row, end_col, start_row, start_col)
    min_distance = d_to_start[end_row][end_col]
    assert d_to_start[end_row][end_col] == d_to_end[start_row][start_col]

    print(f"{min_distance = }")
    print(f"{len(path1) = }, {len(path2) = }")
    print(f"{len(set(path1)) = }, {len(set(path2)) = }")

    counter = 0

    for (row, col) in path1:
        # cheat from here
        cheat_locations = get_radius(grid, row, col, 20)
        for cl_row, cl_col in cheat_locations:
            # print(distances[row][col], distances[cl_row][cl_col])
            total_distance = d_to_start[row][col] + d_to_end[cl_row][cl_col]
            # total_distance = d_to_end[row][col] + d_to_start[cl_row][cl_col]
            d = abs(row - cl_row) + abs(col - cl_col)
            if min_distance - (total_distance + d) >= required_saves:
                counter += 1

        # print("trying to cheat at", (row, col), len(cheat_locations))

    return counter


def solution(filename: str, required_saves: int) -> int:
    grid, start_row, start_col, end_row, end_col = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col,required_saves)


if __name__ == "__main__":
    # print(solution("./example.txt", 50))  # 285?
    print(solution("./input.txt", 100))  # 0
