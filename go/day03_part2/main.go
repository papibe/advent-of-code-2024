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
	regex := regexp.MustCompile(`mul\((\d+),(\d+)\)|do\(\)|don't\(\)`)
	matches := regex.FindAllStringSubmatch(data, -1)

	enable := true

	for _, m := range matches {
		if m[0] == "don't()" {
			enable = false
		} else if m[0] == "do()" {
			enable = true
		} else if enable {
			number0, _ := strconv.Atoi(string(m[1]))
			number1, _ := strconv.Atoi(string(m[2]))
			total_sum += number0 * number1
		}
	}
	return total_sum
}

func solution(filename string) int {
	data := parse(filename)
	return solve(data)
}

func main() {
	fmt.Println(solution("./example2.txt")) // 48
	fmt.Println(solution("./input.txt"))    // 67269798
}
