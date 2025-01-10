from collections import defaultdict
from typing import DefaultDict, List, Set, Tuple


def parse(filename: str) -> DefaultDict[str, List[str]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    graph: DefaultDict[str, List[str]] = defaultdict(list)
    for line in data:
        player1, player2 = line.split("-")
        graph[player1].append(player2)
        graph[player2].append(player1)

    return graph


def solve(graph: DefaultDict[str, List[str]]) -> int:
    teams: Set[Tuple[str, str, str]] = set()
    for p in graph:
        for q in graph[p]:
            for r in graph[q]:
                b1: bool = p in graph[q] and p in graph[r]
                b2: bool = q in graph[p] and q in graph[r]
                b3: bool = r in graph[p] and r in graph[q]
                mutual: bool = b1 and b2 and b3

                if mutual and p != q and p != r and q != p:
                    if p.startswith("t") or q.startswith("t") or r.startswith("t"):
                        s: Tuple[str, str, str] = tuple(sorted((p, q, r)))  # type: ignore
                        teams.add(s)

    return len(teams)


def solution(filename: str) -> int:

    data: DefaultDict[str, List[str]] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 7
    print(solution("./input.txt"))  # 1075
