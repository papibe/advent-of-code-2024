package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	"strings"
)

func parse(filename string) *DefaultDictLambda[string, *Set[string], func() *Set[string]] {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	default_function := func() *Set[string] { return NewSet[string]() }

	graph := NewDefaultDictLambda[string, *Set[string], func() *Set[string]](default_function)

	for _, line := range lines {
		split_line := strings.Split(line, "-")
		player1, player2 := split_line[0], split_line[1]

		graph.get(player1).add(player2)
		graph.get(player2).add(player1)
	}

	return graph
}

func bors_kerbosch(
	R, P, X *Set[string],
	G *DefaultDictLambda[string, *Set[string], func() *Set[string]],
	C *[][]string,
) {

	if P.len() == 0 && X.len() == 0 {
		if R.len() > 0 {
			R_elements := R.list_of_elements()
			sort.Strings(R_elements)
			*C = append(*C, R_elements)
		}
		return
	}

	current_max := math.MinInt
	var pivot string

	for v := range P.union(X).elements {
		v_nodes := G.get(v)
		length := v_nodes.len()
		if length > current_max {
			current_max = length
			pivot = v
		}
	}

	P2 := P.difference(G.get(pivot))

	for s := range P2.elements {
		single := NewSet[string]()
		single.add(s)

		bors_kerbosch(
			R.union(single), P.intersection(G.get(s)), X.intersection(G.get(s)), G, C,
		)
		P.remove(s)
		X.add(s)
	}
}

func solve(graph *DefaultDictLambda[string, *Set[string], func() *Set[string]]) string {
	cliques := [][]string{}

	graph_keys := NewSet[string]()
	for key := range graph.dict {
		graph_keys.add(key)
	}

	bors_kerbosch(NewSet[string](), graph_keys, NewSet[string](), graph, &cliques)

	max_len := math.MinInt
	max_clique := []string{}

	for _, clique := range cliques {
		if len(clique) > max_len {
			max_len = len(clique)
			max_clique = clique
		}
	}
	sort.Strings(max_clique)

	return strings.Join(max_clique, ",")
}

func solution(filename string) string {
	graph := parse(filename)
	return solve(graph)
}

func main() {
	fmt.Println(solution("./example.txt")) // co,de,ka,ta
	fmt.Println(solution("./input.txt"))   // az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy
}
