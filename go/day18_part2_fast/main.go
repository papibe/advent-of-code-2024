package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const INVALID = -1

type Byte struct {
	x int
	y int
}

type Point struct {
	row int
	col int
}

type QueueState struct {
	point Point
	steps int
}

func parse(filename string, fallen int) (*Set[Byte], *[]Byte) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	fallen_bytes := NewSet[Byte]()
	for index := range fallen {
		str_numbers := strings.Split(lines[index], ",")
		x, _ := strconv.Atoi(str_numbers[0])
		y, _ := strconv.Atoi(str_numbers[1])
		fallen_bytes.add(Byte{x, y})
	}

	remaining_bytes := []Byte{}
	for index := fallen; index < len(lines); index++ {
		str_numbers := strings.Split(lines[index], ",")
		x, _ := strconv.Atoi(str_numbers[0])
		y, _ := strconv.Atoi(str_numbers[1])
		remaining_bytes = append(remaining_bytes, Byte{x, y})
	}

	return fallen_bytes, &remaining_bytes
}

func run(fallen_bytes *Set[Byte], remaining_bytes *[]Byte, index, size int) int {
	// BFS setup
	start_point := Point{0, 0}

	queue := NewQueue[QueueState]()
	queue.append(QueueState{start_point, 0})

	visited := NewSet[Point]()
	visited.add(start_point)

	// update walls from previos indexes
	previously_fallen_bytes := NewSet[Byte]()
	for i := range index + 1 {
		previously_fallen_bytes.add((*remaining_bytes)[i])
	}

	// BFS
	for !queue.is_empty() {
		state := queue.popleft()
		row, col := state.point.row, state.point.col

		if row == size && col == size {
			return state.steps
		}

		for _, new_point := range []Point{
			{row, col + 1},
			{row, col - 1},
			{row + 1, col},
			{row - 1, col}} {

			if 0 <= new_point.row && new_point.row <= size &&
				0 <= new_point.col && new_point.col <= size {

				if visited.contains(new_point) {
					continue
				}

				if fallen_bytes.contains(Byte{row, col}) ||
					previously_fallen_bytes.contains(Byte{row, col}) {
					continue
				}

				queue.append(QueueState{new_point, state.steps + 1})
				visited.add(new_point)
			}
		}
	}
	return INVALID
}

func solve(fallen_bytes *Set[Byte], remaining_bytes *[]Byte, size int) string {
	lower := 0
	upper := len(*remaining_bytes) - 1

	for lower < upper {
		middle := (lower + upper) / 2
		result := run(fallen_bytes, remaining_bytes, middle, size)

		if result == INVALID {
			upper = middle
		} else {
			lower = middle + 1
		}
	}
	last_byte := (*remaining_bytes)[lower]
	return fmt.Sprintf("%d,%d", last_byte.x, last_byte.y)
}

func solution(filename string, size, fallen int) string {
	fallen_bytes, remaining_bytes := parse(filename, fallen)
	return solve(fallen_bytes, remaining_bytes, size)
}

func main() {
	fmt.Println(solution("./example.txt", 6, 12))  // 6,1
	fmt.Println(solution("./input.txt", 70, 1024)) // 16,44
}
