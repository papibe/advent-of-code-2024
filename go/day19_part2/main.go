package main

import (
	"fmt"
	"os"
	"strings"
)

type MemoKey struct {
	pattern string
	index   int
}

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

func dfs(pattern string, towels []string, index int, memo map[MemoKey]int) int {
	if index > len(pattern) {
		return 0
	}

	if index == len(pattern) {
		return 1
	}
	key := MemoKey{pattern, index}
	value, is_in_memo := memo[key]
	if is_in_memo {
		return value
	}

	ways := 0
	for _, towel := range towels {
		if strings.HasPrefix(pattern[index:], towel) {
			ways += dfs(pattern, towels, index+len(towel), memo)
		}
	}
	memo[key] = ways
	return ways
}

func possible_ways(pattern string, towels []string) int {
	memo := make(map[MemoKey]int)
	return dfs(pattern, towels, 0, memo)
}

func solve(towels, patterns []string) int {
	total_ways := 0

	for _, pattern := range patterns {
		total_ways += possible_ways(pattern, towels)
	}

	return total_ways
}

func solution(filename string) int {
	towels, patterns := parse(filename)
	return solve(towels, patterns)
}

func main() {
	fmt.Println(solution("./example.txt")) // 16
	fmt.Println(solution("./input.txt"))   // 752461716635602
}
