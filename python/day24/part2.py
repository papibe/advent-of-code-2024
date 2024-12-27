import re
from collections import defaultdict, deque, namedtuple
from itertools import combinations
import heapq as hq
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

from topo import topologicalSort

# Operation = namedtuple("Operation", ["var1", "oper", "var2", "res"])
@dataclass
class Operation:
    var1: int
    oper: str
    var2: int
    res: str

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

def bin_sum(inputs, operations):
    results = {}
    for k, v in inputs.items():
        results[k] = v
    
    # remops = operations
    done = []
    while True:
        change = False
        for o in operations:
            if o.var1 in results and o.var2 in results and o.res not in results:
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
                change = True
        
        if not change:
            break
        

    # if len(done) != len(operations):
    #     print(f"{len(done) = }, {len(operations) = }")
    #     return [], False
    return get_bin(results, "z"), True


def build_adj_list(operations):
    all_symbols_set = set()
    for i, o in enumerate(operations):
        all_symbols_set.add(o.var1)
        all_symbols_set.add(o.var2)
        all_symbols_set.add(o.res)
    
    all_symbols = list(all_symbols_set)
    adj = [[] for _ in range(len(all_symbols))]
    trans = {}
    for i, s in enumerate(all_symbols):
        trans[s] = i

    for o in operations:
        adj[trans[o.res]].append(trans[o.var1])
        adj[trans[o.res]].append(trans[o.var2])

    return adj



def get_bin(inputs, var_name):
    bin_str = deque([])
    for n in range(100):
        if f"{var_name}{n:02d}" not in inputs:
            break
        # bin_str.appendleft(str(inputs[f"{var_name}{n:02d}"]))
        bin_str.append(inputs[f"{var_name}{n:02d}"])
    return bin_str


def test2(x, y, inputs, operations):
    # x = get_bin(inputs, "x")
    # y = get_bin(inputs, "y")
    # assert len(x) == len(y)
    z, ok = bin_sum(inputs, operations)
    if not ok:
        return -1, False
    # print(z)
    # assert len(x) + 1 == len(z)

    i = 0
    carry = 0
    while i < len(x):
        # print(i)
        bsum = x[i] + y[i] + carry
        res = bsum % 2 
        ncarry = 1 if bsum > 1 else 0
        if res != z[i]:
            print(f"fail at {i}, {carry=} {x[i]=}, {y[i]=}, {res=}, {ncarry=}, {z[i]=}")
            return i, False    
        carry = ncarry
        i += 1
    if carry == 0:
        return -1, True
    
    if carry == z[i]:
        return i, True
    else:
        return i, False


def get_dependencies(operations, symbol):
    queue = deque([symbol])
    dependencies = []
    while queue:
        symbol = queue.popleft()
        for o in operations:
            if o.res == symbol:
                if o.var1 not in dependencies:
                    queue.append(o.var1)
                    dependencies.append(o.var1)
                
                if o.var2 not in dependencies:
                    queue.append(o.var2)
                    dependencies.append(o.var2)

    return dependencies

def solve(inputs, operations):
    output = []
    o1 = operations[4]   
    o2 = operations[169]
    output.append(o1.res)
    output.append(o2.res)
    o1.res, o2.res = o2.res, o1.res

    o1 = operations[16]   
    o2 = operations[172]
    output.append(o1.res)
    output.append(o2.res)
    o1.res, o2.res = o2.res, o1.res

    o1 = operations[200]   
    o2 = operations[205]
    output.append(o1.res)
    output.append(o2.res)
    o1.res, o2.res = o2.res, o1.res

    o1 = operations[101]   
    o2 = operations[149]
    output.append(o1.res)
    output.append(o2.res)
    o1.res, o2.res = o2.res, o1.res

    output.sort()
    print(",".join(output))


    def to_number(x):
        rx = [str(n) for n in reversed(x)]
        return int("".join(rx), 2)

    def test(x_value, y_value, operations):
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
            print(f"at {i}: {x_value=}, {y_value=} should be: {x_value+y_value} but is {z_value=}")
            print(f"x  {x_value:045b}")
            print(f"y  {y_value:045b}")
            print(f"z {z_value:046b}")
            return False
    
        return True

    for i in range(45):
        x_value = 1 << i
        y_value = 1 << i
        test(x_value, 0, operations)
        test(x_value, y_value, operations)
        test(0, y_value, operations)
        x_value = (1 << i) -1
        y_value = 1
        test(x_value, y_value, operations)


    return
    moperations = [
        operations[3],
        operations[20],
        operations[34],
        operations[51],
        operations[60],
        operations[68],
        operations[79],
        operations[87],
        operations[89],
        operations[101], #
        operations[106],
        operations[118],
        operations[129],
        operations[138],
        operations[149], #
        operations[159],
        operations[174],
        operations[192],
        operations[213],
        operations[218],
    ]

    indexes = list(range(len(moperations)))
    for index1, index2 in combinations(indexes, 2):

        print(index1, index2)

        o1 = moperations[index1]   
        o2 = moperations[index2]
        o1.res, o2.res = o2.res, o1.res

        a = True
        for i in range(34, 45):
            x_value = 1 << i
            y_value = 1 << i
            a = a and test(x_value, 0, operations)
            a = a and test(x_value, y_value, operations)
            a = a and test(0, y_value, operations)
            x_value = (1 << i) -1
            y_value = 1
            a = a and test(x_value, y_value, operations)

        if a:
            print(f"found {index1}, {index2}")
            print(f"found {o1}, {o2}")

        o1.res, o2.res = o2.res, o1.res



    return 0
    while True:

        i, ok = test(inputs, operations)
        if not ok:
            print(f"{i = }")

        indexes = list(range(len(operations)))
        for index1, index2 in combinations(indexes, 2):

            print(index1, index2)

            o1 = operations[index1]   
            o2 = operations[index2]
            o1.res, o2.res = o2.res, o1.res

            i2, ok = test(inputs, operations)

            if ok: 
                return o1, o2
            else:
                if i2 > i:
                    print(f"{i = }")
                    return o1, o2                    
            o1.res, o2.res = o2.res, o1.res


        

def solution(filename: str) -> int:
    inputs, operations = parse(filename)
    return solve(inputs, operations)


if __name__ == "__main__":
    # print(solution("./example.txt"))  #
    # print(solution("./example1.txt"))  #
    print(solution("./input.txt"))  # 
