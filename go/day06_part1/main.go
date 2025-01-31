package main

import (
	"fmt"
	"os"
	"strings"
)

var INITIAL_DIRECTION = []int{-1, 0}

const GUARD = '^'
const SPACE = '.'

func parse(filename string) (int, int, [][]rune) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	// build grid and get guard initial position
	grid := [][]rune{}
	var initial_row int
	var initial_col int

	for row, line := range lines {
		new_row := []rune{}

		for col, char := range line {
			// record initial position and replce it with space
			if char == GUARD {
				initial_row = row
				initial_col = col
				new_row = append(new_row, SPACE)
			} else {
				new_row = append(new_row, char)
			}
		}
		grid = append(grid, new_row)
	}

	return initial_row, initial_col, grid
}

func solve(initial_row, initial_col int, grid [][]rune) int {
	current_row := initial_row
	current_col := initial_col
	dir_row := INITIAL_DIRECTION[0]
	dir_col := INITIAL_DIRECTION[1]

	visited := make(map[[2]int]bool)

	for {
		next_row := current_row + dir_row
		next_col := current_col + dir_col
		if !(0 <= next_row && next_row < len(grid) &&
			0 <= next_col && next_col < len(grid[0])) {
			return len(visited)
		}
		if grid[next_row][next_col] == SPACE {
			current_row = next_row
			current_col = next_col
		} else {
			dir_row, dir_col = dir_col, -dir_row
		}
		// rotation 90 degrees right
		visited[[2]int{current_row, current_col}] = true
	}
}

func solution(filename string) int {
	initial_row, initial_col, grid := parse(filename)
	return solve(initial_row, initial_col, grid)
}

func main() {
	fmt.Println(solution("./example.txt")) // 41
	fmt.Println(solution("./input.txt"))   // 4656
}
