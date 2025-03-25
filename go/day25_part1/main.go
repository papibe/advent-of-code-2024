package main

import (
	"fmt"
	"os"
	"strings"
)

func parse(filename string) ([][]string, [][]string) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	locks := [][]string{}
	keys := [][]string{}

	for _, block := range blocks {
		if block[0] == '#' {
			locks = append(locks, strings.Split(block, "\n"))
		} else if block[0] == '.' {
			keys = append(keys, strings.Split(block, "\n"))
		} else {
			panic("Invalid input format")
		}
	}

	return locks, keys
}

func build_counter(size int) []int {
	counter_slice := make([]int, size)
	for i := range size {
		counter_slice[i] = -1
	}
	return counter_slice
}

func get_heights(devices [][]string) [][]int {
	heights := [][]int{}
	for _, device := range devices {
		height := build_counter(len(device[0]))

		for col := range len(device[0]) {
			for row := range len(device) {
				if device[row][col] == '#' {
					height[col] += 1
				}
			}
		}
		heights = append(heights, height)
	}
	return heights
}

func solve(locks, keys [][]string) int {
	// get heights
	lock_heights := get_heights(locks)
	key_heights := get_heights(keys)

	// count overall keys and locks fits
	key_lock_fits := 0
	for _, key_height := range key_heights {
		for _, lock_height := range lock_heights {

			pin_problem := false
			for col := range 5 {
				key_pin := key_height[col]
				lock_pin := lock_height[col]

				if key_pin+lock_pin > 5 {
					pin_problem = true
					break
				}
			}
			if !pin_problem {
				key_lock_fits++
			}
		}
	}
	return key_lock_fits
}

func solution(filename string) int {
	locks, keys := parse(filename)
	return solve(locks, keys)
}

func main() {
	fmt.Println(solution("./example.txt")) // 3
	fmt.Println(solution("./input.txt"))   // 3127
}
