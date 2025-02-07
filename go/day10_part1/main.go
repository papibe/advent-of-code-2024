package main

import (
	"fmt"
	"os"
	"strings"
)

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

	score := 0
	for _, trailhead := range trailheads {
		// BFS init
		queue := NewQueue()
		visited := NewVisitedSet()

		queue.push(trailhead)
		visited.add(trailhead)

		// BFS
		for !queue.is_empty() {
			trailhead := queue.pop()
			slope := topo_map[trailhead.row][trailhead.col]
			if slope == 9 {
				score++
				continue
			}

			for _, step := range [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
				step_row, step_col := step[0], step[1]

				new_row := trailhead.row + step_row
				new_col := trailhead.col + step_col

				if 0 <= new_row && new_row < len(topo_map) &&
					0 <= new_col && new_col < len(topo_map[0]) {
					new_slope := topo_map[new_row][new_col]

					new_point := Point{new_row, new_col}
					if new_slope == slope+1 && !visited.contains(new_point) {
						queue.push(new_point)
						visited.add(new_point)
					}
				}
			}
		}

	}
	return score
}

func solution(filename string) int {
	topo_map := parse(filename)
	return solve(topo_map)
}

func main() {
	fmt.Println(solution("./example.txt")) // 36
	fmt.Println(solution("./input.txt"))   // 611
}
