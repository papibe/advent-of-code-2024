package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

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
	// move robots 100 times
	for range 100 {
		for _, robot := range robots {
			robot.col = mod(robot.col+robot.vcol, cols)
			robot.row = mod(robot.row+robot.vrow, rows)
		}
	}

	// count robots in all 4 quadrants
	q1, q2, q3, q4 := 0, 0, 0, 0
	for _, r := range robots {
		if r.row < rows/2 && r.col < cols/2 {
			q1 += 1
		} else if r.row < rows/2 && r.col > cols/2 {
			q2 += 1
		} else if r.row > rows/2 && r.col < cols/2 {
			q3 += 1
		} else if r.row > rows/2 && r.col > cols/2 {
			q4 += 1
		}
	}
	return q1 * q2 * q3 * q4
}

func solution(filename string, rows, cols int) int {
	robots := parse(filename)
	return solve(robots, rows, cols)
}

func main() {
	fmt.Println(solution("./example.txt", 7, 11))  // 12
	fmt.Println(solution("./input.txt", 103, 101)) // 224357412
}
