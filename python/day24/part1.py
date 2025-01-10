import re
from collections import namedtuple
from typing import Dict, List, Tuple

Inputs = Dict[str, int]
Operation = namedtuple("Operation", ["var1", "oper", "var2", "res"])


def parse(filename: str) -> Tuple[Inputs, List[Operation]]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    inputs: Inputs = {}
    for line in blocks[0].splitlines():
        parts = line.split(":")
        var = parts[0]
        value = int(parts[1].strip())
        inputs[var] = value

    regex: str = r"(\w+) (\w+) (\w+) -> (\w+)"
    operations: List[Operation] = []
    for line in blocks[1].splitlines():
        matches = re.match(regex, line)
        assert matches is not None
        var1 = matches.group(1)
        oper = matches.group(2)
        var2 = matches.group(3)
        res = matches.group(4)
        operations.append(Operation(var1, oper, var2, res))

    return inputs, operations


def solve(inputs: Inputs, operations: List[Operation]) -> int:
    results: Dict[str, int] = {}
    for k, v in inputs.items():
        results[k] = v

    reminding_operations = operations
    done: List[Operation] = []
    res: int

    # run through operations
    while reminding_operations:
        reminding_operations = []
        for oper in operations:
            if oper in done:
                continue
            if oper.var1 not in results or oper.var2 not in results:
                reminding_operations.append(oper)
                continue
            if oper.oper == "AND":
                res = results[oper.var1] & results[oper.var2]
            elif oper.oper == "OR":
                res = results[oper.var1] | results[oper.var2]
            elif oper.oper == "XOR":
                res = results[oper.var1] ^ results[oper.var2]
            else:
                raise RuntimeError("operation not supported")

            results[oper.res] = res
            done.append(oper)

    # build binary string
    bin_str: List[str] = []
    for index in reversed(range(50)):
        if f"z{index:02d}" in results:
            bin_str.append(str(results[f"z{index:02d}"]))

    return int("".join(bin_str), 2)


def solution(filename: str) -> int:
    inputs, operations = parse(filename)
    return solve(inputs, operations)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 4
    print(solution("./example1.txt"))  # 2024
    print(solution("./input.txt"))  # 60614602965288
