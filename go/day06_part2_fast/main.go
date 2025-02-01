package main

import (
	"fmt"
	"os"
	"strings"
)

var INITIAL_DIRECTION = []int{-1, 0}

const GUARD = '^'
const SPACE = '.'
const OBSTABLE = '#'

type State struct {
	row  int
	col  int
	drow int
	dcol int
}

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

func first_round(
	grid [][]rune, current_row, current_col, dir_row, dir_col int,
) (map[State]bool, map[[2]int]State) {

	visited := make(map[State]bool)
	previous := make(map[[2]int]State)

	state := State{current_row, current_col, dir_row, dir_col}
	_, ok := visited[state]
	for !ok {
		visited[state] = true

		next_row := current_row + dir_row
		next_col := current_col + dir_col
		if !(0 <= next_row && next_row < len(grid) &&
			0 <= next_col && next_col < len(grid[0])) {
			return visited, previous
		}
		if grid[next_row][next_col] == SPACE {
			position := [2]int{next_row, next_col}
			_, is_in_previous := previous[position]
			if !is_in_previous {
				previous[position] = state
			}

			current_row = next_row
			current_col = next_col
		} else {
			// rotation 90 degrees right
			dir_row, dir_col = dir_col, -dir_row
		}

		state = State{current_row, current_col, dir_row, dir_col}
		_, ok = visited[state]
	}

	return visited, previous
}

func round(grid [][]rune, current_row, current_col, dir_row, dir_col int) bool {
	visited := make(map[State]bool)

	state := State{current_row, current_col, dir_row, dir_col}
	_, ok := visited[state]
	for !ok {
		visited[state] = true

		next_row := current_row + dir_row
		next_col := current_col + dir_col
		if !(0 <= next_row && next_row < len(grid) &&
			0 <= next_col && next_col < len(grid[0])) {
			return false
		}
		if grid[next_row][next_col] == SPACE {
			current_row = next_row
			current_col = next_col
		} else {
			// rotation 90 degrees right
			dir_row, dir_col = dir_col, -dir_row
		}

		state = State{current_row, current_col, dir_row, dir_col}
		_, ok = visited[state]
	}

	return true
}

func solve(initial_row, initial_col int, grid [][]rune) int {
	current_row := initial_row
	current_col := initial_col
	dir_row := INITIAL_DIRECTION[0]
	dir_col := INITIAL_DIRECTION[1]

	// initial guard round
	visited, previous := first_round(grid, current_row, current_col, dir_row, dir_col)

	// form a set of unique locations
	guard_path := make(map[[2]int]bool)
	for state := range visited {
		guard_path[[2]int{state.row, state.col}] = true
	}
	delete(guard_path, [2]int{initial_row, initial_col})

	total := 0
	for position := range guard_path {
		row, col := position[0], position[1]
		grid[row][col] = OBSTABLE

		state := previous[[2]int{row, col}]

		if round(grid, state.row, state.col, state.drow, state.dcol) {
			total++
		}

		grid[row][col] = SPACE
	}
	return total
}

func solution(filename string) int {
	initial_row, initial_col, grid := parse(filename)
	return solve(initial_row, initial_col, grid)
}

func main() {
	fmt.Println(solution("./example.txt")) // 6
	fmt.Println(solution("./input.txt"))   // 1575
}
