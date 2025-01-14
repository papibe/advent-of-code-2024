package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) [][]int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	reports := [][]int{}

	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		report := []int{}
		for _, num_str := range strings.Split(line, " ") {
			num, _ := strconv.Atoi(num_str)
			report = append(report, num)
		}
		reports = append(reports, report)
	}
	return reports
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func is_valid(report []int) bool {
	if report[0] == report[1] {
		return false
	}

	var decreasing bool
	if report[0] < report[1] {
		decreasing = true
	} else {
		decreasing = false
	}

	for i := 0; i < len(report)-1; i++ {
		current := report[i]
		next := report[i+1]

		if decreasing && current > next {
			return false
		}
		if !decreasing && current < next {
			return false
		}
		abs_diff := abs(current - next)
		if !(1 <= abs_diff && abs_diff <= 3) {
			return false
		}
	}

	return true
}

func solve(reports [][]int) int {
	valid_reports := 0

	for _, report := range reports {
		if is_valid(report) {
			valid_reports++
		}
	}
	return valid_reports
}

func solution(filename string) int {
	reports := parse(filename)
	return solve(reports)
}

func main() {
	fmt.Println(solution("./example.txt")) // 2
	fmt.Println(solution("./input.txt"))   // 483
}
