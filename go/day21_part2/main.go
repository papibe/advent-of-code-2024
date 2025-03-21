package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	START = 'S'
	END   = 'E'
	WALL  = '#'
	SPACE = '.'
)

const INVALID = -1

var NUM_KEYPAD = []string{"789", "456", "123", "#0A"}
var DIR_KEYPAD = []string{"#^A", "<v>"}

type Pad []string
type Paths map[rune]Pad

type Position struct {
	row int
	col int
}

type NextPosition struct {
	row int
	col int
	dir string
}

type QueueElement struct {
	position Position
	distance int
	paths    string
}

type MemoQueue struct {
	from  rune
	to    rune
	level int
}

func parse(filename string) Pad {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}

	return strings.Split(strings.Trim(string(data), "\n"), "\n")
}

func get_paths(start_row, start_col int, pad Pad) Paths {
	initial_position := Position{start_row, start_col}

	ways := make(Paths)
	costs := NewDefaultDict[Position, int](math.MaxInt)
	queue := NewQueue[QueueElement]()

	queue.append(QueueElement{initial_position, 0, ""})
	costs.insert(initial_position, 0)
	ways[rune(pad[start_row][start_col])] = []string{""}

	for !queue.is_empty() {
		status := queue.popleft()
		row, col := status.position.row, status.position.col

		for _, next_move := range []NextPosition{
			{row + 1, col, "v"},
			{row - 1, col, "^"},
			{row, col + 1, ">"},
			{row, col - 1, "<"},
		} {
			new_position := Position{next_move.row, next_move.col}

			if 0 <= next_move.row && next_move.row < len(pad) &&
				0 <= next_move.col && next_move.col < len(pad[0]) {

				if pad[next_move.row][next_move.col] == WALL {
					continue
				}

				new_distance := status.distance + 1
				current_keypad := rune(pad[next_move.row][next_move.col])
				if new_distance < costs.get(new_position) {
					costs.insert(new_position, new_distance)
					queue.append(QueueElement{new_position, new_distance, status.paths + next_move.dir})

					ways[current_keypad] = []string{status.paths + next_move.dir}

				} else if new_distance == costs.get(new_position) {
					ways[current_keypad] = append(ways[current_keypad], status.paths+next_move.dir)
					queue.append(QueueElement{new_position, new_distance, status.paths + next_move.dir})
				}
			}
		}
	}

	return ways
}

func build_numpad_paths(pad Pad) map[rune]Paths {
	paths := make(map[rune]Paths)
	for row, line := range pad {
		for col, item := range line {
			if item != WALL {
				paths[item] = get_paths(row, col, pad)
			}
		}
	}
	return paths
}

func product(l [][]string) [][]string {
	// cartesian product
	if len(l) == 2 {
		output := [][]string{}
		for _, e1 := range l[0] {
			for _, e2 := range l[1] {
				output = append(output, []string{e1, e2})
			}
		}
		return output
	}

	output := [][]string{}
	for _, element := range l[0] {
		results := product(l[1:])
		for _, result := range results {
			new_combo := append([]string{element}, result...)
			output = append(output, new_combo)
		}
	}
	return output
}

func get_num_pad(code string, num_paths map[rune]Paths) []string {

	sols := [][]string{}
	prev := 'A'
	for _, char := range code {
		local_sol := []string{}
		for _, path := range num_paths[prev][char] {
			local_sol = append(local_sol, path+"A")
		}
		sols = append(sols, local_sol)
		prev = char
	}

	fsols := product(sols)
	output := []string{}
	for _, sol := range fsols {
		output = append(output, strings.Join(sol, ""))
	}
	return output
}

func _get_dir_pad(
	from, to rune, dir_paths map[rune]Paths, level int, memo map[MemoQueue]int,
) int {
	if level == 1 {
		return len(dir_paths[from][to][0])
	}

	key := MemoQueue{from, to, level}
	cashed_value, ok := memo[key]
	if ok {
		return cashed_value
	}

	best_result := math.MaxInt
	for _, path := range dir_paths[from][to] {
		result := 0
		prev := 'A'
		for _, char := range path {
			x := _get_dir_pad(prev, char, dir_paths, level-1, memo)
			result += x
			prev = char
		}
		best_result = min(best_result, result)
	}
	memo[key] = best_result
	return best_result
}

func get_dir_pad(from, to rune, pad_paths map[rune]Paths, intake_level int) int {
	memo := make(map[MemoQueue]int)

	return _get_dir_pad(from, to, pad_paths, intake_level, memo)
}

func solve(codes []string, numpad_paths, dirpad_paths map[rune]Paths) int {
	total_sum := 0

	for _, code := range codes {
		initial_seq := get_num_pad(code, numpad_paths)

		best_result := math.MaxInt
		for _, sol := range initial_seq {
			result := 0
			prev := 'A'
			for _, char := range sol {
				x := get_dir_pad(prev, char, dirpad_paths, 25)
				result += x
				prev = char
			}
			best_result = min(best_result, result)
		}
		code_numeric_value, _ := strconv.Atoi(code[:len(code)-1])
		total_sum += best_result * code_numeric_value
	}

	return total_sum
}

func solution(filename string) int {
	codes := parse(filename)

	// build paths from every button to another
	numpad_paths := build_numpad_paths(NUM_KEYPAD)
	dirpad_paths := build_numpad_paths(DIR_KEYPAD)

	// patch paths because we have 2 diff functions for pads
	for _, d := range dirpad_paths {
		for k2, paths := range d {
			new_paths := []string{}
			for _, path := range paths {
				new_paths = append(new_paths, path+"A")
			}
			d[k2] = new_paths
		}
	}

	return solve(codes, numpad_paths, dirpad_paths)
}

func main() {
	fmt.Println(solution("./input.txt")) // 167389793580400
}
