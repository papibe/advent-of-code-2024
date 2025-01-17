from collections import defaultdict
from typing import DefaultDict, List, Set


def parse(filename: str) -> DefaultDict[str, List[str]]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    graph: DefaultDict[str, List[str]] = defaultdict(list)
    for line in data:
        player1, player2 = line.split("-")
        graph[player1].append(player2)
        graph[player2].append(player1)

    return graph


def bors_kerbosch_v2(
    R: Set[str],
    P: Set[str],
    X: Set[str],
    G: DefaultDict[str, List[str]],
    C: List[List[str]],
) -> None:

    if len(P) == 0 and len(X) == 0:
        if len(R) > 0:
            C.append(sorted(R))
        return

    (d, pivot) = max([(len(G[v]), v) for v in P.union(X)])

    for v in P.difference(G[pivot]):
        bors_kerbosch_v2(
            R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C
        )
        P.remove(v)
        X.add(v)


def solve(graph: DefaultDict[str, List[str]]) -> str:
    cliques: List[List[str]] = []
    bors_kerbosch_v2(set(), set(graph.keys()), set(), graph, cliques)

    max_len: int = float("-inf")  # type: ignore
    max_clique: List[str] = []
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
            max_clique = clique

    return ",".join(sorted(max_clique))


def solution(filename: str) -> str:
    data: DefaultDict[str, List[str]] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # co,de,ka,ta
    print(solution("./input.txt"))  # az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy
