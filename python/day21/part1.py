from collections import defaultdict, deque
from typing import DefaultDict, Deque, Dict, List, Tuple

Pad = List[str]
Cost = DefaultDict[Tuple[int, int], int]
Queue = Deque[Tuple[int, int, int, str]]
Paths = Dict[str, List[str]]
Memo = Dict[Tuple[str, str], List[str]]
Sequences = List[str]


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    return data


NUM_KEYPAD: Pad = ["789", "456", "123", "#0A"]

DIR_KEYPAD: Pad = [
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
                new_distance = distance + 1
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


memo1: Memo = {}
memo2: Memo = {}
memo3: Memo = {}


def get_num_pad(
    code: str, from_: str, pad_path: Dict[str, Paths], memo: Memo
) -> List[str]:
    if not code:
        return [""]

    key: Tuple[str, str] = (code, from_)
    if key in memo:
        return memo[key]

    results: List[str] = []
    char: str = code[0]
    for sol in pad_path[from_][char]:
        result = get_num_pad(code[1:], char, pad_path, memo)
        for res in result:
            results.append(sol + "A" + res)

    memo[key] = results
    return results


def solve(
    data: List[str], num_paths: Dict[str, Paths], dir_paths: Dict[str, Paths]
) -> int:
    total_sum: int = 0

    for code in data:
        initial_seq: Sequences = get_num_pad(code, "A", num_paths, memo1)

        # pruning longer sequences
        min_len: int = min([len(s) for s in initial_seq])
        initial_seq = [s for s in initial_seq if len(s) == min_len]

        dir_pad_seq1: Sequences = []
        for sol in initial_seq:
            dp: Sequences = get_num_pad(sol, "A", dir_paths, memo2)
            dir_pad_seq1.extend(dp)

        # pruning longer sequences
        min_len = min([len(s) for s in dir_pad_seq1])
        dir_pad_seq1 = [s for s in dir_pad_seq1 if len(s) == min_len]

        dir_pad_seq2: Sequences = []
        for sol in dir_pad_seq1:
            dp = get_num_pad(sol, "A", dir_paths, memo3)
            dir_pad_seq2.extend(dp)

        min_len = min([len(s) for s in dir_pad_seq2])
        numeric_code: int = int(code[:-1])

        total_sum += min_len * numeric_code

    return total_sum


def solution(filename: str) -> int:
    data: List[str] = parse(filename)

    # build paths from every button to another
    numpad_paths: Dict[str, Paths] = build_numpad_paths(NUM_KEYPAD)
    dirpad_paths: Dict[str, Paths] = build_numpad_paths(DIR_KEYPAD)

    return solve(data, numpad_paths, dirpad_paths)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 126384
    print(solution("./input.txt"))  # 138560
