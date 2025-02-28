package main

import (
	"fmt"
	"os"
	"sort"
	"strings"
)

type Points []Point

func (a Points) Len() int      { return len(a) }
func (a Points) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
func (a Points) Less(i, j int) bool {
	if a[i].row < a[j].row {
		return true
	}
	if a[i].row > a[j].row {
		return false
	}
	return a[i].col < a[j].col
}

type Point struct {
	row int
	col int
}

const (
	Up    = '^'
	Down  = 'v'
	Left  = '<'
	Right = '>'
)

const (
	Robot       = '@'
	Space       = '.'
	Wall        = '#'
	Box         = 'O'
	BigBoxLeft  = '['
	BigBoxRight = ']'
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
			switch char {
			case Wall:
				warehouse_row = append(warehouse_row, Wall)
				warehouse_row = append(warehouse_row, Wall)
			case Box:
				warehouse_row = append(warehouse_row, BigBoxLeft)
				warehouse_row = append(warehouse_row, BigBoxRight)
			case Space:
				warehouse_row = append(warehouse_row, Space)
				warehouse_row = append(warehouse_row, Space)
			case Robot:
				warehouse_row = append(warehouse_row, Robot)
				warehouse_row = append(warehouse_row, Space)
			default:
				panic("Unknow input character")

			}
		}
		warehouse = append(warehouse, warehouse_row)
	}

	// get robot position
	var robot_row, robot_col int
outer_loop:
	for row, warehouse_row := range warehouse {
		for col, cell := range warehouse_row {
			if cell == Robot {
				robot_row = row
				robot_col = col
				break outer_loop
			}
		}
	}

	// patch position of robot
	warehouse[robot_row][robot_col] = Space

	// join movement lines
	movement_blocks := append([]string{}, strings.Split(blocks[1], "\n")...)
	movements := strings.Join(movement_blocks, "")

	return warehouse, movements, robot_row, robot_col
}

func specialmove(warehouse Warehouse, row, col, row_dir, col_dir int) (int, int) {
	// Move up and down and push potentially a buch of boxes
	next_row := row + row_dir
	next_col := col + col_dir

	if warehouse[next_row][next_col] == Space {
		return next_row, next_col
	}

	if warehouse[next_row][next_col] == Wall {
		return row, col
	}

	// BFS init
	starting_point := Point{row, col}
	queue := NewQueue[Point]()
	queue.append(starting_point)

	affected := NewSet[Point]()
	affected.add(starting_point)

	// BFS
	for !queue.is_empty() {
		current := queue.popleft()

		next_row := current.row + row_dir
		next_col := current.col + col_dir

		if warehouse[next_row][next_col] == Wall {
			return row, col
		}

		if warehouse[next_row][next_col] == BigBoxRight {
			queue.append(Point{next_row, next_col})
			queue.append(Point{next_row, next_col - 1})

			affected.add(Point{next_row, next_col})
			affected.add(Point{next_row, next_col - 1})

		} else if warehouse[next_row][next_col] == BigBoxLeft {
			queue.append(Point{next_row, next_col})
			queue.append(Point{next_row, next_col + 1})

			affected.add(Point{next_row, next_col})
			affected.add(Point{next_row, next_col + 1})
		}
	}

	for !affected.is_empty() {
		// sort affected points
		affected_points := affected.list_of_elemets()
		sort.Sort(Points(affected_points))

		for _, affected_point := range affected_points {
			nr := affected_point.row + row_dir
			nc := affected_point.col + col_dir

			if !affected.contains(Point{nr, nc}) {
				warehouse[nr][nc] = warehouse[affected_point.row][affected_point.col]
				warehouse[affected_point.row][affected_point.col] = Space
				affected.remove(Point{affected_point.row, affected_point.col})
			}
		}
	}

	return row + row_dir, col + col_dir
}

func movement(warehouse Warehouse, row, col, row_dir, col_dir int) (int, int) {
	// Execute the actual movement on the grid. Including pusing boxes
	if row_dir != 0 {
		return specialmove(warehouse, row, col, row_dir, col_dir)
	}

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
			if cell == BigBoxLeft {
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
	fmt.Println(solution("./example2.txt")) // 9021
	fmt.Println(solution("./input.txt"))    // 1481392
}
