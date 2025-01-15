package main

import (
	"fmt"
	"os"
	"strings"
)

var STEPS = [][]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {-1, -1}, {-1, 1}, {1, 1}, {1, -1}}

func parse(filename string) []string {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	return strings.Split(strings.Trim(string(data), "\n"), "\n")
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func solve(puzzle []string) int {
	total := 0

	for row, line := range puzzle {
		for col, _ := range line {

			// go all directions
			for _, dirs := range STEPS {
				dir_row := dirs[0]
				dir_col := dirs[1]
				new_row, new_col := row, col

				// when chose a direction check if matches the word
				did_break := false
				for _, char := range "XMAS" {
					if 0 <= new_row && new_row < len(puzzle) &&
						0 <= new_col && new_col < len(puzzle[0]) &&
						char == rune(puzzle[new_row][new_col]) {

						new_row += dir_row
						new_col += dir_col
					} else {
						did_break = true
						break
					}
				}
				if !did_break {
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
	fmt.Println(solution("./example.txt")) // 18
	fmt.Println(solution("./input.txt"))   // 2434
}
