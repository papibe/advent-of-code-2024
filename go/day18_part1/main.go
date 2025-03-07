package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

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

func parse(filename string, fallen int) *Set[Byte] {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	bytes := NewSet[Byte]()
	for index := range fallen {
		str_numbers := strings.Split(lines[index], ",")
		x, _ := strconv.Atoi(str_numbers[0])
		y, _ := strconv.Atoi(str_numbers[1])
		bytes.add(Byte{x, y})
	}

	return bytes
}

func solve(bytes *Set[Byte], size int) int {
	// BFS setup
	start_point := Point{0, 0}

	queue := NewQueue[QueueState]()
	queue.append(QueueState{start_point, 0})

	visited := NewSet[Point]()
	visited.add(start_point)

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

				if bytes.contains(Byte{row, col}) {
					continue
				}

				queue.append(QueueState{new_point, state.steps + 1})
				visited.add(new_point)
			}
		}
	}
	return -1
}

func solution(filename string, size, fallen int) int {
	bytes := parse(filename, fallen)
	return solve(bytes, size)
}

func main() {
	fmt.Println(solution("./example.txt", 6, 12))  // 22
	fmt.Println(solution("./input.txt", 70, 1024)) // 272
}
