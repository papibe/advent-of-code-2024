from collections import defaultdict, deque
from itertools import product
from typing import DefaultDict, Deque, Dict, List, Tuple

Pad = List[str]
Cost = DefaultDict[Tuple[int, int], int]
Queue = Deque[Tuple[int, int, int, str]]
Paths = Dict[str, List[str]]
Memo = Dict[Tuple[str, str, int], int]
Sequences = List[str]


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    return data


NUM_KEYPAD = ["789", "456", "123", "#0A"]


DIR_KEYPAD = [
    "#^A",
    "<v>",
]


def get_paths(start_row: int, start_col: int, pad: Pad) -> Paths:
    ways: Paths = {}
    costs: Cost = defaultdict(lambda: float("inf"))  # type: ignore
    queue: Queue = deque([(start_row, start_col, 0, "")])
    costs[(start_row, start_col)] = 0
    ways[pad[start_row][start_col]] = [""]

    while queue:
        row, col, distance, paths = queue.popleft()
        for new_row, new_col, dir in [
            (row + 1, col, "v"),
            (row - 1, col, "^"),
            (row, col + 1, ">"),
            (row, col - 1, "<"),
        ]:
            if 0 <= new_row < len(pad) and 0 <= new_col < len(pad[0]):
                if pad[new_row][new_col] == "#":
                    continue
                new_distance: int = distance + 1
                if new_distance < costs[(new_row, new_col)]:
                    costs[(new_row, new_col)] = new_distance
                    queue.append((new_row, new_col, new_distance, paths + dir))

                    ways[pad[new_row][new_col]] = [paths + dir]

                elif new_distance == costs[(new_row, new_col)]:
                    ways[pad[new_row][new_col]].append(paths + dir)
                    queue.append((new_row, new_col, new_distance, paths + dir))

    return ways


def build_numpad_paths(pad: Pad) -> Dict[str, Paths]:
    paths: Dict[str, Paths] = {}
    for row, line in enumerate(pad):
        for col, item in enumerate(line):
            if item != "#":
                paths[item] = get_paths(row, col, pad)

    return paths


def get_num_pad(code: str, numpad: Dict[str, Paths]) -> List[str]:

    sols: List[List[str]] = []
    prev: str = "A"
    for char in code:
        local_sol = []
        for path in numpad[prev][char]:
            local_sol.append(path + "A")
        sols.append(local_sol)
        prev = char

    fsols: List[Tuple[str]] = product(*sols)  # type: ignore
    otuput: List[str] = []
    for sol in fsols:
        otuput.append("".join(sol))
    return otuput


def get_dir_pad(
    from_: str, to: str, dirpath: Dict[str, Paths], intake_level: int
) -> int:

    memo: Memo = {}

    def _get_dir_pad(from_: str, to: str, level: int) -> int:
        if level == 1:
            return len(dirpath[from_][to][0])

        key: Tuple[str, str, int] = (from_, to, level)
        if key in memo:
            return memo[key]

        best_result: int = float("inf")  # type: ignore
        for path in dirpath[from_][to]:
            result = 0
            prev = "A"
            for char in path:
                result += _get_dir_pad(prev, char, level - 1)
                prev = char

            best_result = min(best_result, result)

        memo[key] = best_result
        return best_result

    return _get_dir_pad(from_, to, intake_level)


def solve(data: List[str], numpad: Dict[str, Paths], dirpath: Dict[str, Paths]) -> int:
    total_sum: int = 0

    for code in data:

        sols = get_num_pad(code, numpad)

        best_result: int = float("inf")  # type: ignore
        for sol in sols:
            result = 0
            prev = "A"
            for char in sol:
                result += get_dir_pad(prev, char, dirpath, 25)
                prev = char
            best_result = min(best_result, result)

        total_sum += best_result * int(code[:-1])

    return total_sum


def solution(filename: str) -> int:
    numpad_paths = build_numpad_paths(NUM_KEYPAD)
    dirpad_paths = build_numpad_paths(DIR_KEYPAD)

    # patch paths because we have 2 diff functions for pads
    for k, v in dirpad_paths.items():
        for k2, paths in v.items():
            new_paths = []
            for path in paths:
                new_paths.append(path + "A")
            v[k2] = new_paths

    data: List[str] = parse(filename)
    return solve(data, numpad_paths, dirpad_paths)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 167389793580400
