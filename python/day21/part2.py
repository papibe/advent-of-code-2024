import re
from collections import deque, defaultdict
from itertools import product
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    return data

NUM_KEYPAD_MAP = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),

    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),

    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),

    "#": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}

NUM_KEYPAD = [
    "789",
    "456",
    "123",
    "#0A"
]

DIR_KEYPAD_MAP = {
    "#": (0, 0),
    "^": (0, 1),
    "A": (0, 2),

    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

DIR_KEYPAD = [
    "#^A",
    "<v>",
]

def get_paths(start_row, start_col, pad):
    ways = {}
    costs = defaultdict(lambda: float("inf"))
    queue = deque([(start_row, start_col, 0, "")])
    costs[(start_row, start_col)] = 0
    ways[pad[start_row][start_col]] = [""]

    while queue:
        row, col, distance, paths = queue.popleft()
        for new_row, new_col, dir in [
            (row + 1, col, "v"),
            (row - 1, col, "^"),
            (row, col + 1, ">"),
            (row, col - 1, "<")
        ]:
            if 0 <= new_row < len(pad) and 0 <= new_col < len(pad[0]):
                if pad[new_row][new_col] == "#":
                    continue
                new_distance = distance + 1
                if new_distance < costs[(new_row, new_col)]:

                    # print(costs[(new_row, new_col)], new_distance)
                    costs[(new_row, new_col)] = new_distance
                    queue.append((new_row, new_col, new_distance, paths + dir))

                    ways[pad[new_row][new_col]] = [paths + dir]
                elif new_distance == costs[(new_row, new_col)]:
                    ways[pad[new_row][new_col]].append(paths + dir)
                    queue.append((new_row, new_col, new_distance, paths + dir))
                    
    return ways


def build_numpad_paths(pad):
    paths = {}
    for row, line in enumerate(pad):
        for col, item in enumerate(line):
            if item != "#":
                paths[item] = get_paths(row, col, pad)
                # break

    # for k,v in paths.items():
    #     print(k, v)
    #     print()

    return paths

def get_num_pad(code, numpad):

    sols = []
    prev = "A"
    for char in code:
        local_sol = []
        for path in numpad[prev][char]:
            local_sol.append(path + "A")
        sols.append(local_sol)
        prev = char
    fsols = product(*sols)
    otuput = []
    for sol in fsols:
        otuput.append("".join(sol))
    return otuput


memo = {}

def get_dir_pad(from_, to, dirpath, intake_level):
    
    def _get_dir_pad(from_, to, level):
        if level == 1:
            return len(dirpath[from_][to][0])

        key = (from_, to, level)
        if key in memo:
            return memo[key]

        best_result = float("inf")
        # print(f"{dirpath[from_][to] = }")
        for path in dirpath[from_][to]:
            # print(from_, to, path, level)
            result = 0
            prev = "A"
            for char in path:
                result += _get_dir_pad(prev, char, level - 1)
                prev = char

            # print(f"{result = }")
            best_result = min(best_result, result)

        memo[key] = best_result
        return best_result

    return _get_dir_pad(from_, to, intake_level)



def solve(data: str, numpad, dirpath) -> int:
    total_sum: int = 0
        
    for code in data:
 
        sols = get_num_pad(code, numpad)

        best_result = float("inf")
        for sol in sols:
            print(sol)
            result = 0
            prev = "A"
            counter = 0
            for char in sol:
                r = get_dir_pad(prev, char, dirpath, 25)
                # print("  ", prev, char, r)
                result += r
                prev = char
                # counter += 1
                # if counter == 2:
                #     break
            # print("result", result)
            best_result = min(best_result, result)
            # break

        print(code, best_result)

        total_sum += best_result * int(code[:-1])

    return total_sum


def solution(filename: str) -> int:
    numpad_paths = build_numpad_paths(NUM_KEYPAD)
    # print(numpad_paths)
    # return 0
    dirpad_paths = build_numpad_paths(DIR_KEYPAD)
    dirpaths = {}
    for k, v in dirpad_paths.items():
        for k2, paths in v.items():
            new_paths = []
            for path in paths:
                new_paths.append(path + "A")

            v[k2] = new_paths

    # for k, v in dirpad_paths.items():
    #     print(k, v)

    data: str = parse(filename)
    return solve(data, numpad_paths, dirpad_paths)
    # return 0


if __name__ == "__main__":
    print(solution("./input.txt"))  # 167389793580400
