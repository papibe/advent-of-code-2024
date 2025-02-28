package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

const (
	Start = 'S'
	End   = 'E'
	Wall  = '#'
)

type Grid []string

type DijkstraQueue struct {
	row     int
	col     int
	dir_row int
	dir_col int
	cost    int
}

type Point struct {
	row, col int
}

func parse(filename string) (Grid, int, int, int, int) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	grid := strings.Split(strings.Trim(string(data), "\n"), "\n")

	var start_row, start_col, end_row, end_col int

	// find start and end
	for row, line := range grid {
		for col, cell := range line {
			if cell == Start {
				start_row = row
				start_col = col
			} else if cell == End {
				end_row = row
				end_col = col
			}
		}
	}

	return grid, start_row, start_col, end_row, end_col
}

func solve(grid Grid, start_row, start_col, end_row, end_col int) int {
	// setup costs for dijkstra
	costs := [][]int{}
	for range len(grid) {
		costs_row := []int{}
		for range len(grid[0]) {
			costs_row = append(costs_row, math.MaxInt)
		}
		costs = append(costs, costs_row)
	}

	queue := NewQueue[DijkstraQueue]()
	queue.append(DijkstraQueue{start_row, start_col, 0, 1, 0})

	// Dijkstra
	for !queue.is_empty() {
		item := queue.popleft()

		for _, step := range []Point{
			{item.dir_row, item.dir_col},
			{item.dir_col, -item.dir_row},
			{-item.dir_col, item.dir_row},
		} {
			new_row := item.row + step.row
			new_col := item.col + step.col

			if grid[new_row][new_col] == Wall {
				continue
			}

			var new_cost int
			if item.dir_row == step.row && item.dir_col == step.col {
				new_cost = item.cost + 1
			} else {
				new_cost = item.cost + 1001
			}

			if new_cost < costs[new_row][new_col] {
				costs[new_row][new_col] = new_cost
				queue.append(
					DijkstraQueue{new_row, new_col, step.row, step.col, new_cost})
			}
		}
	}

	return costs[end_row][end_col]
}

func solution(filename string) int {
	grid, start_row, start_col, end_row, end_col := parse(filename)
	return solve(grid, start_row, start_col, end_row, end_col)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 7036
	fmt.Println(solution("./example2.txt")) // 11048
	fmt.Println(solution("./input.txt"))    // 102488
}
