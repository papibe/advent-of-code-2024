package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type State struct {
	stone     int
	reminding int
}

var memo = make(map[State]int)

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

func blink(stone int, reminding int) int {
	if reminding == 0 {
		return 1
	}
	state := State{stone, reminding}
	cached_value, in_memo := memo[state]
	if in_memo {
		return cached_value
	}

	var result int

	if stone == 0 {
		result = blink(1, reminding-1)
	} else {
		str_stone := strconv.Itoa(stone)
		stone_len := len(str_stone)

		if stone_len%2 == 0 {
			first_str := str_stone[:stone_len/2]
			second_str := str_stone[stone_len/2:]

			first, _ := strconv.Atoi(first_str)
			second, _ := strconv.Atoi(second_str)

			result = blink(first, reminding-1) + blink(second, reminding-1)
		} else {
			result = blink(stone*2024, reminding-1)
		}
	}
	memo[state] = result
	return result
}

func solve(stones []int) int {
	size := 0
	for _, stone := range stones {
		size += blink(stone, 75)
	}
	return size
}

func solution(filename string) int {
	stones := parse(filename)
	return solve(stones)

}

func main() {
	fmt.Println(solution("./input.txt")) // 276661131175807
}
