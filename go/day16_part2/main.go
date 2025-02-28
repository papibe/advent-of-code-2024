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

func solve(grid Grid, start, end Point) int {
	initial_state := State{start, Point{0, 1}}

	// setup costs for dijkstra
	costs := NewDefaultDict[State, int](math.MaxInt)
	costs.insert(initial_state, 0)

	prev := NewDefaultDict[State, Set[State]](*NewSet[State]())

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
			new_point := Point{point.row + step.row, point.col + step.col}

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

				prev_state := NewSet[State]()
				prev_state.add(State{point, dir})
				prev.insert(new_state, *prev_state)

				queue.append(QueueState{new_state, new_cost})
			} else if new_cost == previous_cost {
				prev_state := prev.get(new_state)
				prev_state.add(State{point, dir})
			}
		}
	}

	// get min score to get to the end
	min_score := math.MaxInt
	for _, step := range []Point{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		min_score = min(min_score, costs.get(State{end, step}))
	}

	// get endpoints
	min_ends := []State{}
	for _, step := range []Point{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
		if costs.get(State{end, step}) == min_score {
			min_ends = append(min_ends, State{end, step})
		}
	}

	//reverse walk
	queue_for_path := NewQueue[State]()
	good_seats_position := NewSet[State]()
	for _, min_end := range min_ends {
		queue_for_path.append(min_end)
		good_seats_position.add(min_end)
	}

	for !queue_for_path.is_empty() {
		end := queue_for_path.pop()
		for seat, _ := range prev.get(end).visited {
			if !good_seats_position.contains(seat) {
				queue_for_path.append(seat)
				good_seats_position.add(seat)
			}
		}
	}

	good_seats := NewSet[Point]()
	for position, _ := range good_seats_position.visited {
		good_seats.add(position.point)
	}

	return good_seats.len()
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
