package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func parse(filename string) string {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	return string(data)
}

func solve(data string) int {
	total_sum := 0
	regex := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	matches := regex.FindAllStringSubmatch(data, -1)

	for _, m := range matches {
		number0, _ := strconv.Atoi(string(m[1]))
		number1, _ := strconv.Atoi(string(m[2]))
		total_sum += number0 * number1
	}
	return total_sum
}

func solution(filename string) int {
	data := parse(filename)
	return solve(data)
}

func main() {
	fmt.Println(solution("./example1.txt")) // 161
	fmt.Println(solution("./input.txt"))    // 188741603
}
