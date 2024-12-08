package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) ([]int, []int) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	left_locations := []int{}
	right_locations := []int{}

	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	for _, line := range lines {
		numbers := strings.Split(line, "   ")
		left, _ := strconv.Atoi(numbers[0])
		right, _ := strconv.Atoi(numbers[1])

		left_locations = append(left_locations, left)
		right_locations = append(right_locations, right)
	}

	return left_locations, right_locations
}

func solve(left_locations, right_locations []int) int {
	// calculate frequencies on the right side
	frequencies := make(map[int]int)
	for _, n := range right_locations {
		value, ok := frequencies[n]
		if !ok {
			frequencies[n] = 0

		}
		frequencies[n] = value + 1
	}

	// calculate score
	score := 0
	for _, left := range left_locations {
		frequency, is_in_right_side := frequencies[left]
		if is_in_right_side {
			score += left * frequency
		}
	}
	return score
}

func solution(filename string) int {
	left_locations, right_locations := parse(filename)
	return solve(left_locations, right_locations)
}

func main() {
	fmt.Println(solution("./example.txt")) // 31
	fmt.Println(solution("./input.txt"))   // 22962826
}
