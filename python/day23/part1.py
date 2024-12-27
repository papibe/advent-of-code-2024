import re
from collections import defaultdict
from typing import List, Tuple


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    graph = defaultdict(list)
    for line in data:
        player1, player2 = line.split("-")
        graph[player1].append(player2)
        graph[player2].append(player1)

    return graph


def solve(graph) -> int:
    teams = set()
    for p in graph:
        for q in graph[p]:
            for r in graph[q]:
                b1 = p in graph[q] and p in graph[r]
                b2 = q in graph[p] and q in graph[r]
                b3 = r in graph[p] and r in graph[q]
                mutual = b1 and b2 and b3

                if mutual and p != q and p != r and q != p:
                    if (p.startswith("t") or q.startswith("t") or r.startswith("t")):
                        s = tuple(sorted((p, q, r)))
                        teams.add(s)

    return len(teams)


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 7
    print(solution("./input.txt"))  # 1075
