import re
from collections import defaultdict, deque, namedtuple
import heapq as hq
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

Operation = namedtuple("Operation", ["var1", "oper", "var2", "res"])

def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        blocks: str = fp.read().split("\n\n")


    inputs = {}
    for line in blocks[0].splitlines():
        parts = line.split(":")
        var = parts[0]
        value = int(parts[1].strip())
        inputs[var] = value

    regex = r"(\w+) (\w+) (\w+) -> (\w+)"
    operations = []
    for line in blocks[1].splitlines():
        matches = re.match(regex, line)
        assert matches is not None
        var1 = matches.group(1)
        oper = matches.group(2)
        var2 = matches.group(3)
        res = matches.group(4)
        operations.append(Operation(var1, oper, var2, res))

    # print(operations)

    return inputs, operations


def solve(inputs, operations) -> int:
    total_sum: int = 0

    results = {}
    for k, v in inputs.items():
        results[k] = v
    
    remops = operations
    done = []
    while remops:
        remops = []
        for o in operations:
            if o in done:
                continue
            if o.var1 not in results or o.var2 not in results:
                remops.append(o)
                continue
            if o.oper == "AND":
                r = results[o.var1] & results[o.var2]
            elif o.oper == "OR":
                r = results[o.var1] | results[o.var2]
            elif o.oper == "XOR":
                r = results[o.var1] ^ results[o.var2]
            else:
                raise RuntimeError("bla")
            
            results[o.res] = r
            done.append(o)

    results = {}
    for k, v in inputs.items():
        results[k] = v

    for o in done:
        if o.oper == "AND":
            r = results[o.var1] & results[o.var2]
        elif o.oper == "OR":
            r = results[o.var1] | results[o.var2]
        elif o.oper == "XOR":
            r = results[o.var1] ^ results[o.var2]
        else:
            raise RuntimeError("bla")
        
        results[o.res] = r


    # print(results)
    bin_str = deque([])
    for n in range(100):
        if f"z{n:02d}" not in results:
            break
        bin_str.appendleft(str(results[f"z{n:02d}"]))

    print(bin_str)

    return int("".join(bin_str), 2)


def solution(filename: str) -> int:
    inputs, operations = parse(filename)
    return solve(inputs, operations)


if __name__ == "__main__":
    print(solution("./example.txt"))  #
    print(solution("./example1.txt"))  #
    print(solution("./input.txt"))  # 
