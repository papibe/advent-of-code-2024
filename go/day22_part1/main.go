package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) []int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")
	numbers := []int{}

	for _, line := range lines {
		number, _ := strconv.Atoi(line)
		numbers = append(numbers, number)
	}
	return numbers
}

func pseudo_round(n int) int {
	n = (n ^ (n * 64)) % 16777216
	n = (n ^ (n / 32)) % 16777216
	n = (n ^ (n * 2048)) % 16777216
	return n
}

func pseudo_random(n int) int {
	for range 2000 {
		n = pseudo_round(n)
	}
	return n
}

func solve(numbers []int) int {
	total_sum := 0

	for _, number := range numbers {
		total_sum += pseudo_random(number)
	}
	return total_sum
}

func solution(filename string) int {
	numbers := parse(filename)
	return solve(numbers)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 37327623
	fmt.Println(solution("./input.txt"))    // 21147129593
}
