package main

import (
	"fmt"
)

const INVALID = -1

func get_combo(operand, a, b, c int) int {
	if 0 <= operand && operand <= 3 {
		return operand
	} else if operand == 4 {
		return a
	} else if operand == 5 {
		return b
	} else if operand == 6 {
		return c
	}
	return -1
}

func dfs(program []int, index, value int) int {
	// reverse enginieered from program.txt

	if index < 0 {
		return value
	}
	for octal_digit := range 8 {
		a := (value << 3) + octal_digit
		b := a % 8
		b = b ^ 1
		c := a >> b
		b = b ^ 4
		b = b ^ c
		output := b % 8

		if output == program[index] {
			next_value := dfs(program, index-1, a)
			if next_value != INVALID {
				return next_value
			}
		}

	}
	return INVALID
}

func solution(program []int) int {
	return dfs(program, len(program)-1, 0)
}

func main() {

	fmt.Println(
		solution([]int{2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0}),
	) // 202356708354602
}
