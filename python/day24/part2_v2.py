import re
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Set, Tuple

ALL_GOOD: int = -1


@dataclass
class Operation:
    var1: str
    oper: str
    var2: str
    res: str

    def __hash__(self) -> int:
        return hash("f{self.var1}-{self.oper}-{self.var2}-{self.res}")


def parse(filename: str) -> Tuple[Dict[str, int], List[Operation]]:
    # divide input into 2 blocks
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    # parse inputs
    inputs: Dict[str, int] = {}
    for line in blocks[0].splitlines():
        parts = line.split(":")
        var = parts[0]
        value = int(parts[1].strip())
        inputs[var] = value

    # parse oprations
    regex = r"(\w+) (\w+) (\w+) -> (\w+)"
    operations: List[Operation] = []
    for line in blocks[1].splitlines():
        matches = re.match(regex, line)
        assert matches is not None
        var1: str = matches.group(1)
        oper: str = matches.group(2)
        var2: str = matches.group(3)
        res: str = matches.group(4)
        operations.append(Operation(var1, oper, var2, res))

    return inputs, operations


def bin_sum(
    inputs: Dict[str, int], operations: List[Operation]
) -> Tuple[List[int], bool]:
    results: Dict[str, int] = {}
    for k, v in inputs.items():
        results[k] = v

    while True:
        change: bool = False
        for o in operations:
            if o.var1 in results and o.var2 in results and o.res not in results:
                if o.oper == "AND":
                    r = results[o.var1] & results[o.var2]
                elif o.oper == "OR":
                    r = results[o.var1] | results[o.var2]
                elif o.oper == "XOR":
                    r = results[o.var1] ^ results[o.var2]
                else:
                    raise RuntimeError(f"{o.oper}: operation not supported")

                results[o.res] = r
                change = True

        if not change:
            break

    return get_bin(results, "z"), True


def get_bin(inputs: Dict[str, int], var_name: str) -> List[int]:
    bin_list: List[int] = []
    for n in range(100):
        if f"{var_name}{n:02d}" not in inputs:
            break
        bin_list.append(inputs[f"{var_name}{n:02d}"])
    return bin_list


def get_moperations(operations: List[Operation], index: int) -> List[Operation]:
    moperations: Set[Operation] = set()

    initial_results: Set[str] = {
        f"z{index - 1:02d}",
        f"z{index:02d}",
        f"z{index + 1:02d}",
    }

    for o in operations:
        if o.res in initial_results:
            moperations.add(o)

    vars = set()
    for o in moperations:
        vars.add(o.var1)
        vars.add(o.var2)

    for o in operations:
        if o.var1 in vars or o.var2 in vars or o.res in vars:
            moperations.add(o)

    for o in moperations:
        vars.add(o.var1)
        vars.add(o.var2)
        vars.add(o.res)

    for o in operations:
        if o.var1 in vars or o.var2 in vars or o.res in vars:
            moperations.add(o)

    return list(moperations)


def to_number(x: List[int]) -> int:
    rx: List[str] = [str(n) for n in reversed(x)]
    return int("".join(rx), 2)


def test(x_value: int, y_value: int, operations: List[Operation], index: int) -> bool:
    x = list(reversed([int(s) for s in f"{x_value:045b}"]))
    y = list(reversed([int(s) for s in f"{y_value:045b}"]))
    inputs = {}
    for idx in range(45):
        inputs[f"x{idx:02d}"] = x[idx]
        inputs[f"y{idx:02d}"] = y[idx]
    z, ok = bin_sum(inputs, operations)
    if not ok:
        print("not ok: ")
    z_value = to_number(z)
    if x_value + y_value != z_value:
        # print(
        #     f"at {index}: {x_value=}, {y_value=} should be: {x_value+y_value} but is {z_value=}"
        # )
        # print(f"x  {x_value:045b}")
        # print(f"y  {y_value:045b}")
        # print(f"z {z_value:046b}")
        return False

    return True


def get_error_at_index(operations: List[Operation], min_index: int, max_index: int) -> int:
    for i in range(min_index, max_index):
        tests_ok: bool = True
        power_of_2: int = 1 << i

        tests_ok = tests_ok and test(power_of_2, 0, operations, i)
        tests_ok = tests_ok and test(0, power_of_2, operations, i)
        tests_ok = tests_ok and test(power_of_2, power_of_2, operations, i)

        just_ones: int = (1 << i) - 1
        tests_ok = tests_ok and test(just_ones, 1, operations, i)

        if not (tests_ok):
            return i

    return -1


def solve(inputs: Dict[str, int], operations: List[Operation]) -> str:
    output: List[str] = []

    index: int = get_error_at_index(operations, 0, 45)
    while index != ALL_GOOD:
        print(f"Problem detected at index {index}")

        moperations = get_moperations(operations, index)
        print(f"Operations considered for swapping: {len(moperations)}")

        indexes = list(range(len(moperations)))
        for index1, index2 in combinations(indexes, 2):

            # swap operations
            o1 = moperations[index1]
            o2 = moperations[index2]
            o1.res, o2.res = o2.res, o1.res

            if get_error_at_index(operations, index - 1, index + 3) == ALL_GOOD:
                print("fixing by swaping:")
                print(f"  {o1}")
                print(f"  {o2}")
                print()
                output.append(o1.res)
                output.append(o2.res)
                break

            o1.res, o2.res = o2.res, o1.res

        index = get_error_at_index(operations, index, 45)

    output.sort()
    return ",".join(output)


def solution(filename: str) -> str:
    inputs, operations = parse(filename)
    return solve(inputs, operations)


if __name__ == "__main__":

    result = solution("./input.txt")
    print(result)  #
    assert result == "cgr,hpc,hwk,qmd,tnt,z06,z31,z37"
