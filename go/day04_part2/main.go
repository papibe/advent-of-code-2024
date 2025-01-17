package main

import (
	"fmt"
	"os"
	"strings"
)

var STEPS = [][]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {-1, -1}, {-1, 1}, {1, 1}, {1, -1}}

var PATTERNS = [][][]rune{
	{
		{'M', '.', 'S'},
		{'.', 'A', '.'},
		{'M', '.', 'S'},
	},
	{
		{'M', '.', 'M'},
		{'.', 'A', '.'},
		{'S', '.', 'S'},
	},
	{
		{'S', '.', 'S'},
		{'.', 'A', '.'},
		{'M', '.', 'M'},
	},
	{
		{'S', '.', 'M'},
		{'.', 'A', '.'},
		{'S', '.', 'M'},
	},
}

func parse(filename string) [][]rune {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	puzzle := [][]rune{}

	for _, line := range strings.Split(strings.Trim(string(data), "\n"), "\n") {
		puzzle = append(puzzle, []rune(line))
	}

	return puzzle
}

func check(puzzle [][]rune, start_row, start_col int, pattern [][]rune) bool {
	for row, line := range pattern {
		for col, char := range line {
			if char == '.' {
				continue
			}
			data_row := start_row + row
			data_col := start_col + col
			if !(0 <= data_row && data_row < len(puzzle) &&
				0 <= data_col && data_col < len(puzzle[0])) {
				return false
			}
			s := puzzle[data_row]
			if char != s[data_col] {
				return false
			}
		}
	}

	return true
}

func solve(data [][]rune) int {
	total := 0

	for row, line := range data {
		for col, _ := range line {
			for _, pattern := range PATTERNS {
				if check(data, row, col, pattern) {
					total++
				}
			}
		}
	}
	return total
}

func solution(filename string) int {
	puzzle := parse(filename)
	return solve(puzzle)
}

func main() {
	fmt.Println(solution("./example.txt")) // 9
	fmt.Println(solution("./input.txt"))   // 1835
}
