package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const XMAS_FRAME = "+++++++++++++++++++++++++++++++"

type Robot struct {
	col  int
	row  int
	vcol int
	vrow int
}

func parse(filename string) []*Robot {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	re_line := regexp.MustCompile(`p=(\d+),(\d+) v=([0-9\-]+),([0-9\-]+)`)
	robots := []*Robot{}

	for _, line := range lines {
		matches := re_line.FindStringSubmatch(line)

		col, _ := strconv.Atoi(matches[1])
		row, _ := strconv.Atoi(matches[2])
		vcol, _ := strconv.Atoi(matches[3])
		vrow, _ := strconv.Atoi(matches[4])

		robots = append(robots, &Robot{col, row, vcol, vrow})
	}
	return robots
}

func mod(a, b int) int {
	// equivalent function to % in python
	return (a%b + b) % b
}

func solve(robots []*Robot, rows, cols int) int {
	// prep grid for printing
	grid := [][]string{}
	for range rows {
		grid_row := []string{}
		for range cols {
			grid_row = append(grid_row, ".")
		}
		grid = append(grid, grid_row)
	}

	for second := 1; second < 10000; second++ {
		// movement
		for _, robot := range robots {
			robot.col = mod(robot.col+robot.vcol, cols)
			robot.row = mod(robot.row+robot.vrow, rows)
		}

		// draw
		for _, r := range robots {
			grid[r.row][r.col] = "+"
		}

		// check for pattern
		for _, grid_row := range grid {
			grid_row_str := strings.Join(grid_row, "")
			if strings.Contains(grid_row_str, XMAS_FRAME) {
				return second
			}
		}

		// reset grid
		for _, r := range robots {
			grid[r.row][r.col] = "."
		}

	}
	return -1 // not found!
}

func solution(filename string, rows, cols int) int {
	robots := parse(filename)
	return solve(robots, rows, cols)
}

func main() {
	fmt.Println(solution("./input.txt", 103, 101)) // 7083
}
