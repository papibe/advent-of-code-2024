package main

import (
	"fmt"
	"math"
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
	distance int
}

type QueueCheatElement struct {
	position Position
	cheats   int
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

func run(grid [][]rune, start, end Position) (*DefaultDict[Position, int], []Position) {
	// dijkstra setup
	distances := NewDefaultDict[Position, int](math.MaxInt)

	pqueue := NewPriorityQueue[Position]()
	pqueue.Push(start, 0)

	previous := make(map[Position]Position)

	// dijkstra
	for !pqueue.IsEmpty() {
		position, distance := pqueue.Pop()

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

				new_distance := distance + 1
				if new_distance < distances.get(new_position) {
					distances.insert(new_position, new_distance)
					previous[new_position] = position

					pqueue.Push(new_position, new_distance)
				}
			}
		}
	}

	// obtain path to the end by going back from end to start
	path := []Position{}
	current := end
	for current != start {
		path = append(path, current)
		current = previous[current]
	}
	path = append(path, start)

	return distances, path
}

func get_radius(grid [][]rune, position Position, number_of_cheats int) *Set[Position] {
	// BFS init
	queue := NewQueue[QueueCheatElement]()
	queue.append(QueueCheatElement{position, number_of_cheats})

	visited := NewSet[Position]()
	visited.add(position)

	// BFS
	for !queue.is_empty() {
		status := queue.popleft()
		pos := status.position

		if status.cheats <= 0 {
			continue
		}

		for _, new_position := range []Position{
			{pos.row + 1, pos.col},
			{pos.row - 1, pos.col},
			{pos.row, pos.col + 1},
			{pos.row, pos.col - 1},
		} {
			if 0 <= new_position.row && new_position.row < len(grid) &&
				0 <= new_position.col && new_position.col < len(grid[0]) {

				if !visited.contains(new_position) {
					queue.append(QueueCheatElement{new_position, status.cheats - 1})
					visited.add(new_position)
				}
			}
		}
	}

	// get cheat destinations
	cheat_destinations := NewSet[Position]()
	for pos, _ := range visited.visited {
		if grid[pos.row][pos.col] != WALL {
			distance := abs(position.row-pos.row) + abs(position.col-pos.col)
			if distance != 0 {
				cheat_destinations.add(pos)
			}
		}
	}
	return cheat_destinations
}

func abs(a int) int {
	if a > 0 {
		return a
	}
	return -a
}

func solve(grid [][]rune, start, end Position, required_saves, cheat_allowed int) int {
	distance_to_start, path := run(grid, start, end)
	distance_to_end, _ := run(grid, end, start)
	min_distance := distance_to_start.get(end)

	counter := 0
	for _, position := range path {
		// cheat fromt here
		cheat_positions := get_radius(grid, position, cheat_allowed)
		for cheat_pos, _ := range cheat_positions.visited {
			total_distance := distance_to_start.get(position) +
				distance_to_end.get(cheat_pos)
			distance := abs(position.row-cheat_pos.row) +
				abs(position.col-cheat_pos.col)
			if min_distance-(total_distance+distance) >= required_saves {
				counter++
			}
		}
	}
	return counter
}

func solution(filename string, required_saves, cheat_allowed int) int {
	grid, start, end := parse(filename)
	return solve(grid, start, end, required_saves, cheat_allowed)
}

func main() {
	// it takes 2.6s
	fmt.Println(solution("./input.txt", 100, 20)) // 1014683
}
