import re
from collections import defaultdict
from typing import List, Tuple


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    graph = defaultdict(set)
    for line in data:
        player1, player2 = line.split("-")
        graph[player1].add(player2)
        graph[player2].add(player1)

    return graph


def bors_kerbosch_v1(R, P, X, G, C):

    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return 
    
    for v in P.union(set([])):
        bors_kerbosch_v1(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)


def bors_kerbosch_v2(R, P, X, G, C):

    if len(P) == 0 and len(X) == 0:
        if len(R) > 0:
            C.append(sorted(R))            
        return

    (d, pivot) = max([(len(G[v]), v) for v in P.union(X)])
                     
    for v in P.difference(G[pivot]):
        bors_kerbosch_v2(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)


def solve(graph) -> int:
    C1 = []
    G = graph
    bors_kerbosch_v2(set([]), set(G.keys()), set([]), G, C1)
    
    max_len = float("-inf")
    max_nodes = set()
    for c in C1:
        if len(c) > max_len:
            max_len = len(c)
            max_nodes = c

    return ",".join(sorted(max_nodes))


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example.txt"))  # co,de,ka,ta
    print(solution("./input.txt"))  # az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy
