package main

import (
	"fmt"
	"os"
	"sort"
	"strings"
)

type Team struct {
	player1 string
	player2 string
	player3 string
}

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

func solve(graph *DefaultDictLambda[string, *Set[string], func() *Set[string]]) int {
	teams := NewSet[Team]()

	for p := range graph.dict {
		for q := range graph.get(p).elements {
			for r := range graph.get(q).elements {

				p_neighbors := graph.get(p)
				q_neighbors := graph.get(q)
				r_neighbors := graph.get(r)

				b1 := q_neighbors.contains(p) && r_neighbors.contains(p)
				b2 := p_neighbors.contains(q) && r_neighbors.contains(q)
				b3 := p_neighbors.contains(r) && q_neighbors.contains(r)
				mutual := b1 && b2 && b3

				if mutual && p != q && p != r && q != p {
					if strings.HasPrefix(p, "t") ||
						strings.HasPrefix(q, "t") ||
						strings.HasPrefix(r, "t") {

						team := []string{p, q, r}
						sort.Strings(team)
						teams.add(Team{team[0], team[1], team[2]})
					}
				}
			}
		}
	}
	return teams.len()
}

func solution(filename string) int {
	graph := parse(filename)
	return solve(graph)
}

func main() {
	fmt.Println(solution("./example.txt")) // 7
	fmt.Println(solution("./input.txt"))   // 1075
}
