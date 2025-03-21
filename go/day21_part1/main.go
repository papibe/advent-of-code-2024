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
	code string
	from rune
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

				if pad[next_move.row][next_move.col] == '#' {
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
			if item != '#' {
				paths[item] = get_paths(row, col, pad)
			}
		}
	}
	return paths
}

func get_num_pad(code string, from rune, pad_paths map[rune]Paths, memo map[MemoQueue][]string) []string {
	if code == "" {
		return []string{""}
	}

	key := MemoQueue{code, from}
	cashed_value, ok := memo[key]
	if ok {
		return cashed_value
	}

	results := []string{}
	char := rune(code[0])

	for _, solution := range pad_paths[from][char] {
		result := get_num_pad(code[1:], char, pad_paths, memo)
		for _, res := range result {
			results = append(results, solution+"A"+res)
		}
	}

	memo[key] = results
	return results
}

var memo1 = make(map[MemoQueue][]string)
var memo2 = make(map[MemoQueue][]string)
var memo3 = make(map[MemoQueue][]string)

func solve(codes []string, numpad_paths, dirpad_paths map[rune]Paths) int {
	total_sum := 0

	for _, code := range codes {
		initial_seq := get_num_pad(code, 'A', numpad_paths, memo1)

		// prune longer sequences
		min_len := math.MaxInt
		for _, seq := range initial_seq {
			min_len = min(min_len, len(seq))
		}
		pruned_seq := []string{}
		for _, seq := range initial_seq {
			if len(seq) == min_len {
				pruned_seq = append(pruned_seq, seq)
			}
		}

		dir_pad_seq1 := []string{}
		for _, sol := range pruned_seq {
			dp := get_num_pad(sol, 'A', dirpad_paths, memo2)
			dir_pad_seq1 = append(dir_pad_seq1, dp...)
		}

		// prune longer sequences
		min_len = math.MaxInt
		for _, seq := range dir_pad_seq1 {
			min_len = min(min_len, len(seq))
		}
		pruned_seq = []string{}
		for _, seq := range dir_pad_seq1 {
			if len(seq) == min_len {
				pruned_seq = append(pruned_seq, seq)
			}
		}

		dir_pad_seq2 := []string{}
		for _, sol := range pruned_seq {
			dp := get_num_pad(sol, 'A', dirpad_paths, memo3)
			dir_pad_seq2 = append(dir_pad_seq2, dp...)
		}

		min_len = math.MaxInt
		for _, seq := range dir_pad_seq2 {
			min_len = min(min_len, len(seq))
		}

		numeric_code, _ := strconv.Atoi(code[:len(code)-1])
		total_sum += min_len * numeric_code
	}

	return total_sum
}

func solution(filename string) int {
	codes := parse(filename)

	// build paths from every button to another
	numpad_paths := build_numpad_paths(NUM_KEYPAD)
	dirpad_paths := build_numpad_paths(DIR_KEYPAD)

	return solve(codes, numpad_paths, dirpad_paths)
}

func main() {
	fmt.Println(solution("./example.txt")) // 126384
	fmt.Println(solution("./input.txt"))   // 134120
}
