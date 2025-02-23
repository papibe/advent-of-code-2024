package main

import (
	"fmt"
	"os"
	"strings"
)

const (
	Up    = '^'
	Down  = 'v'
	Left  = '<'
	Right = '>'
)

const (
	Robot = '@'
	Space = '.'
	Wall  = '#'
	Box   = 'O'
)

type Warehouse [][]rune

func parse(filename string) (Warehouse, string, int, int) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	warehouse := Warehouse{}
	for _, line := range strings.Split(blocks[0], "\n") {
		warehouse_row := []rune{}
		for _, char := range line {
			warehouse_row = append(warehouse_row, char)
		}
		warehouse = append(warehouse, warehouse_row)
	}

	// get robot position
	var robot_row, robot_col int
outer_loop:
	for row, warehouse_row := range warehouse {
		for col, cell := range warehouse_row {
			if cell == rune(Robot) {
				robot_row = row
				robot_col = col
				break outer_loop
			}
		}
	}

	// patch position of robot
	warehouse[robot_row][robot_col] = rune(Space)

	// join movement lines
	movement_blocks := append([]string{}, strings.Split(blocks[1], "\n")...)
	movement := strings.Join(movement_blocks, "")

	return warehouse, movement, robot_row, robot_col
}

func movement(warehouse Warehouse, row, col, row_dir, col_dir int) (int, int) {
	// Execute the actual movement on the grid. Including pusing boxes
	next_row := row + row_dir
	next_col := col + col_dir

	if warehouse[next_row][next_col] == Space {
		return next_row, next_col
	}

	if warehouse[next_row][next_col] == Wall {
		return row, col
	}

	// next postition is a box. Finding a space
	current_row := next_row
	current_col := next_col
	for warehouse[current_row][current_col] != Space &&
		warehouse[current_row][current_col] != Wall {
		current_row += row_dir
		current_col += col_dir
	}

	if warehouse[current_row][current_col] == Wall {
		return row, col
	}

	// space behind a box
	for !(current_row == next_row && current_col == next_col) {
		previous_row := current_row - row_dir
		previous_col := current_col - col_dir

		// swap
		warehouse[current_row][current_col],
			warehouse[previous_row][previous_col] = warehouse[previous_row][previous_col],
			warehouse[current_row][current_col]

		current_row = previous_row
		current_col = previous_col
	}

	return current_row, current_col
}

func solve(warehouse Warehouse, movements string, row, col int) int {
	// run movements
	for _, move := range movements {
		switch move {
		case Left:
			row, col = movement(warehouse, row, col, 0, -1)
		case Right:
			row, col = movement(warehouse, row, col, 0, 1)
		case Up:
			row, col = movement(warehouse, row, col, -1, 0)
		case Down:
			row, col = movement(warehouse, row, col, 1, 0)
		default:
			panic("Direction not recognized")
		}
	}
	coordinates_sum := 0
	for wrow, warehouse_row := range warehouse {
		for wcol, cell := range warehouse_row {
			if cell == Box {
				coordinates_sum += (100 * wrow) + wcol
			}
		}
	}

	return coordinates_sum
}

func solution(filename string) int {
	warehouse, movements, robot_row, robot_col := parse(filename)
	return solve(warehouse, movements, robot_row, robot_col)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 2028
	fmt.Println(solution("./example2.txt")) // 10092
	fmt.Println(solution("./input.txt"))    // 1463715
}
