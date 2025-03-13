package main

import (
	"fmt"
	"os"
	"strings"
)

func parse(filename string) ([]string, []string) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	towels := []string{}
	towels = append(towels, strings.Split(blocks[0], ", ")...)

	patterns := strings.Split(blocks[1], "\n")

	return towels, patterns
}

func dfs(pattern string, towels []string, index int) bool {
	if index >= len(pattern) {
		return false
	}

	if index == len(pattern)-1 {
		return true
	}

	for _, towel := range towels {
		if strings.HasPrefix(pattern[index:], towel) {
			if dfs(pattern, towels, index+len(towel)) {
				return true
			}
		}
	}

	return false
}

func is_possible(pattern string, towels []string) bool {
	return dfs(pattern, towels, 0)
}

func solve(towels, patterns []string) int {
	possible := 0

	for _, pattern := range patterns {
		if is_possible(pattern, towels) {
			possible++
		}
	}
	return possible
}

func solution(filename string) int {
	towels, patterns := parse(filename)
	return solve(towels, patterns)
}

func main() {
	fmt.Println(solution("./example.txt")) // 6
	fmt.Println(solution("./input.txt"))   // 265
}
