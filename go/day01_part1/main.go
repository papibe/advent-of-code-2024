package main

import (
	"fmt"
	"os"
	"slices"
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

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func solve(left_locations, right_locations []int) int {
	// sort both locations
	slices.Sort(left_locations)
	slices.Sort(right_locations)

	// calculate distance
	total_distance := 0
	for index := 0; index < len(left_locations); index++ {
		total_distance += abs(right_locations[index] - left_locations[index])
	}
	return total_distance
}

func solution(filename string) int {
	left_locations, right_locations := parse(filename)
	return solve(left_locations, right_locations)
}

func main() {
	fmt.Println(solution("./example.txt")) // 11
	fmt.Println(solution("./input.txt"))   // 2192892
}
