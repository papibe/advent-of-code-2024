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

type Point struct {
	row, col int
}

type State struct {
	point Point
	dir   Point
}
type QueueState struct {
	state State
	cost  int
}

const (
	Forward int = 1
	Reverse int = -1
)

var DIRECTIONS = []Point{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}

func parse(filename string) (Grid, Point, Point) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	grid := strings.Split(strings.Trim(string(data), "\n"), "\n")

	var start, end Point

	// find start and end
	for row, line := range grid {
		for col, cell := range line {
			if cell == Start {
				start = Point{row, col}
			} else if cell == End {
				end = Point{row, col}
			}
		}
	}

	return grid, start, end
}

func dijkstra(grid Grid, start, end, facing Point, direction int) *DefaultDict[State, int] {
	initial_state := State{start, facing}

	// setup costs for dijkstra
	costs := NewDefaultDict[State, int](math.MaxInt)
	costs.insert(initial_state, 0)

	queue := NewQueue[QueueState]()
	queue.append(QueueState{initial_state, 0})

	// Dijkstra
	for !queue.is_empty() {
		current := queue.popleft()
		point := current.state.point
		dir := current.state.dir
		cost := current.cost

		for _, step := range []Point{
			{dir.row, dir.col},
			{dir.col, -dir.row},
			{-dir.col, dir.row},
		} {
			new_point := Point{
				point.row + direction*step.row, point.col + direction*step.col,
			}

			if grid[new_point.row][new_point.col] == Wall {
				continue
			}

			var new_cost int
			if step == dir {
				new_cost = cost + 1
			} else {
				new_point = point
				new_cost = cost + 1000
			}

			new_state := State{new_point, step}
			previous_cost := costs.get(new_state)
			if new_cost < previous_cost {
				costs.insert(new_state, new_cost)
				queue.append(QueueState{new_state, new_cost})
			}
		}
	}
	return costs
}

func solve(grid Grid, start, end Point) int {

	// start -> end
	forward_costs := dijkstra(grid, start, end, Point{0, 1}, Forward)

	// get min score to get to the end
	min_score := math.MaxInt
	for _, step := range DIRECTIONS {
		min_score = min(min_score, forward_costs.get(State{end, step}))
	}

	// get endpoints
	min_ends := []State{}
	for _, step := range DIRECTIONS {
		if forward_costs.get(State{end, step}) == min_score {
			min_ends = append(min_ends, State{end, step})
		}
	}

	// end -> start
	reverse_costs := dijkstra(grid, end, start, min_ends[0].dir, Reverse)

	// get best seats using costs from regular and reverse trips
	seats := NewSet[Point]()
	for _, step := range DIRECTIONS {
		for row := range len(grid) {
			for col := range len(grid[0]) {
				if grid[row][col] == Wall {
					continue
				}
				point := Point{row, col}
				state := State{point, step}
				forward_cost := forward_costs.get(state)
				reverse_cost := reverse_costs.get(state)

				if reverse_cost+forward_cost == min_score {
					seats.add(point)
				}
			}
		}
	}

	return seats.len()
}

func solution(filename string) int {
	grid, start, end := parse(filename)
	return solve(grid, start, end)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 45
	fmt.Println(solution("./example2.txt")) // 64
	fmt.Println(solution("./input.txt"))    // 559
}
