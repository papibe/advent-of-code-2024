package main

import (
	"fmt"
	"os"
	"strings"
)

type Map [][]int

func parse(filename string) Map {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	topo_map := Map{}
	for _, line := range lines {
		row := []int{}
		for _, char := range line {
			number := char - '0'
			row = append(row, int(number))
		}
		topo_map = append(topo_map, row)
	}
	return topo_map
}

func dfs(trailhead Point, visited VisitedSet, topo_map Map) int {
	slope := topo_map[trailhead.row][trailhead.col]

	if slope == 9 {
		return 1
	}

	trail_rating := 0

	for _, step := range [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		step_row, step_col := step[0], step[1]

		new_row := trailhead.row + step_row
		new_col := trailhead.col + step_col

		if 0 <= new_row && new_row < len(topo_map) &&
			0 <= new_col && new_col < len(topo_map[0]) {
			new_slope := topo_map[new_row][new_col]

			new_point := Point{new_row, new_col}
			if new_slope == slope+1 && !visited.contains(new_point) {
				visited.add(new_point)
				trail_rating += dfs(new_point, visited, topo_map)
				visited.remove(new_point)
			}
		}
	}
	return trail_rating
}

func solve(topo_map Map) int {
	// get trailheads
	trailheads := []Point{}
	for row, line := range topo_map {
		for col, trail := range line {
			if trail == 0 {
				trailheads = append(trailheads, Point{row, col})
			}
		}
	}

	rating := 0

	for _, trailhead := range trailheads {
		visited := NewVisitedSet()
		visited.add(trailhead)

		rating += dfs(trailhead, *visited, topo_map)
	}
	return rating
}

func solution(filename string) int {
	topo_map := parse(filename)
	return solve(topo_map)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 81
	fmt.Println(solution("./example2.txt")) // 13
	fmt.Println(solution("./input.txt"))    // 1380
}
