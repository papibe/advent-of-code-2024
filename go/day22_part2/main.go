package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type BestKey struct {
	c1 int
	c2 int
	c3 int
	c4 int
}

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

func solve(numbers []int) int {
	buyers := [][]int{}
	for _, number := range numbers {
		n := pseudo_round(number)
		single_buyer := []int{n}
		for range 2000 {
			n = pseudo_round(n)
			single_buyer = append(single_buyer, n%10)
		}
		buyers = append(buyers, single_buyer)
	}

	best := make(map[BestKey]int)
	for _, b := range buyers {
		seen := NewSet[BestKey]()

		for i := range len(b) - 4 {
			d1, d2, d3, d4, d5 := b[i], b[i+1], b[i+2], b[i+3], b[i+4]
			diff_key := BestKey{d2 - d1, d3 - d2, d4 - d3, d5 - d4}
			if seen.contains(diff_key) {
				continue
			}
			seen.add(diff_key)
			previous_value, ok := best[diff_key]
			if !ok {
				previous_value = 0
			}
			best[diff_key] = previous_value + d5
		}
	}
	best_value := math.MinInt
	for _, value := range best {
		best_value = max(best_value, value)
	}
	return best_value
}

func solution(filename string) int {
	numbers := parse(filename)
	return solve(numbers)
}

func main() {
	fmt.Println(solution("./example2.txt")) // 23
	fmt.Println(solution("./input.txt"))    // 2445
}
