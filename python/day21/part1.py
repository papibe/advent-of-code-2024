import re
from collections import deque, defaultdict
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

saves = [0]
memo1 = {}
memo2 = {}
memo3 = {}

def get_num_pad(code, row, col, pad, pad_path, mappad, memo, level):
    if not code:
        return [""]
    key = (code, row, col)
    # print(key)
    if key in memo:
        # print(' ' * level, "save")
        saves[0] += 1
        return memo[key]
    results = []
    # for char in code:
    char = code[0]
    from_ = pad[row][col]
    # if char == from_:
    #     continue
    # print(f"{' ' * level}{from_ = }, {char = } precal {pad_path[from_][char]}")
    for sol in pad_path[from_][char]:
        result = get_num_pad(code[1:], *mappad[char], pad, pad_path, mappad, memo, level + 1)
        # print(f"{' ' * level}{sol = } {result = }")
        for res in result:
            results.append(sol + "A" +res)
    # print(f"{' ' * level}{results = }")
    memo[key] = results
    return results

def solve(data: str, numpad, dirpath) -> int:
    total_sum: int = 0
        
    for code in data:
        num_row, num_col = NUM_KEYPAD_MAP["A"]
        dir1_row, dir1_col = DIR_KEYPAD_MAP["A"]
        dir2_row, dir2_col = DIR_KEYPAD_MAP["A"]
 

        nsp = get_num_pad(code, num_row, num_col, NUM_KEYPAD, numpad, NUM_KEYPAD_MAP, memo1, 0)

        # for sol in nsp:
        #     assert len(code) == sol.count("A")

        dp1 = []
        for sol in nsp:
            dp = get_num_pad(sol, dir1_row, dir1_col, DIR_KEYPAD, dirpath, DIR_KEYPAD_MAP, memo2, 0)
            # for res in dp:
            #     if len(sol) != res.count("A"):
            #         print(sol)
            #         print(res)
            dp1.extend(dp)
 
        dp2 = []
        for sol in dp1:
            dp = get_num_pad(sol, dir2_row, dir2_col, DIR_KEYPAD, dirpath, DIR_KEYPAD_MAP, memo3, 0)
            # for res in dp:
                # if len(sol) != res.count("A"):
                #     print(sol)
                #     print(res)

            dp2.extend(dp)
 
        # for sol in dp2:
        #     print(sol.count("A"), end="")
        # print()


        # print(f"{dp2 = }")
        # print(f"{len(dp2) = }")

        min_len = min([len(s) for s in dp2])

        digits = []
        for char in code:
            if char.isnumeric():
                digits.append(char)
        numeric = int("".join(digits))

        print(f"{saves = }")
        # print(min_len, numeric)

        total_sum += min_len * numeric

    return total_sum


def solution(filename: str) -> int:
    numpad_paths = build_numpad_paths(NUM_KEYPAD)
    # print(numpad_paths)
    dirpad_paths = build_numpad_paths(DIR_KEYPAD)
    data: str = parse(filename)
    return solve(data, numpad_paths, dirpad_paths)
    # return 0


if __name__ == "__main__":
    print(solution("./example.txt"))  # 126384
    print(solution("./input.txt"))  # 138560
