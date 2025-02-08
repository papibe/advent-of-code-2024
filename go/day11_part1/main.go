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
	stones := []int{}

	for _, line := range lines {
		for _, number_str := range strings.Split(line, " ") {
			number, _ := strconv.Atoi(number_str)
			stones = append(stones, number)
		}
	}
	return stones
}

func blink(stones []int) []int {
	new_stones := []int{}

	for _, stone := range stones {
		if stone == 0 {
			new_stones = append(new_stones, 1)
			continue
		}
		str_stone := strconv.Itoa(stone)
		stone_len := len(str_stone)

		if stone_len%2 == 0 {
			first_str := str_stone[:stone_len/2]
			second_str := str_stone[stone_len/2:]

			first, _ := strconv.Atoi(first_str)
			second, _ := strconv.Atoi(second_str)

			new_stones = append(new_stones, first)
			new_stones = append(new_stones, second)
		} else {
			new_stones = append(new_stones, stone*2024)
		}
	}
	return new_stones
}

func solve(stones []int, n_blinks int) ([]int, int) {
	for range n_blinks {
		stones = blink(stones)
	}
	return stones, len(stones)
}

func solution(filename string, n_blinks int) int {
	stones := parse(filename)
	_, result := solve(stones, n_blinks)
	return result

}

func main() {
	fmt.Println(solution("./example.txt", 25)) // 55312
	fmt.Println(solution("./input.txt", 25))   // 233050
}
