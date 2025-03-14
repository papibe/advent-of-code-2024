package main

import (
	"fmt"
	"os"
	"strings"
)

const (
	START = 'S'
	END   = 'E'
	WALL  = '#'
	SPACE = '.'
)

const INVALID = -1

type Position struct {
	row int
	col int
}

type QueueElement struct {
	position Position
	cost     int
}

func parse(filename string) ([][]rune, Position, Position) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	// form grid
	grid := [][]rune{}
	for _, line := range lines {
		grid_row := []rune(line)
		grid = append(grid, grid_row)
	}

	// get start and end positions
	var start, end Position
	for row := range len(grid) {
		for col := range len(grid[0]) {
			cell := grid[row][col]
			if cell == START {
				start = Position{row, col}
			} else if cell == END {
				end = Position{row, col}
			}
		}
	}

	return grid, start, end
}

func run(grid [][]rune, start, end Position) int {
	// BFS setup
	initial_status := QueueElement{start, 0}
	queue := NewQueue[QueueElement]()
	queue.append(initial_status)

	visited := NewSet[Position]()
	visited.add(initial_status.position)

	// BFS
	for !queue.is_empty() {
		status := queue.popleft()
		position := status.position

		if position == end {
			return status.cost
		}

		for _, new_position := range []Position{
			{position.row + 1, position.col},
			{position.row - 1, position.col},
			{position.row, position.col + 1},
			{position.row, position.col - 1},
		} {
			if 0 <= new_position.row && new_position.row < len(grid) &&
				0 <= new_position.col && new_position.col < len(grid[0]) {

				if grid[new_position.row][new_position.col] == WALL {
					continue
				}

				if !visited.contains(new_position) {
					queue.append(QueueElement{new_position, status.cost + 1})
					visited.add(new_position)
				}
			}

		}
	}

	return INVALID
}

func solve(grid [][]rune, start, end Position) int {
	// brute force
	main_result := run(grid, start, end)
	results := []int{}

	for row, line := range grid {
		for col, cell := range line {
			if cell == WALL {
				grid[row][col] = SPACE
				result := run(grid, start, end)
				grid[row][col] = WALL

				if result != INVALID {
					results = append(results, main_result-result)
				}
			}
		}
	}
	greater_than_threshold := 0
	for _, result := range results {
		if result >= 100 {
			greater_than_threshold++
		}
	}

	return greater_than_threshold
}

func solution(filename string) int {
	grid, start, end := parse(filename)
	return solve(grid, start, end)
}

func main() {
	// it takes ~25secs
	fmt.Println(solution("./input.txt")) // 1417
}
