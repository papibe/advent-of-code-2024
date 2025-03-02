package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

const (
	ADV int = 0
	BXL int = 1
	BST int = 2
	JNZ int = 3
	BXC int = 4
	OUT int = 5
	BDV int = 6
	CDV int = 7
)

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

func solution(a, b, c int, program []int) string {
	pointer := 0
	output := []int{}

	for 0 <= pointer && pointer < len(program) {
		opcode := program[pointer]
		operand := program[pointer+1]

		combo := get_combo(operand, a, b, c)
		literal := operand

		switch opcode {
		case ADV:
			numerator := a
			denominator := math.Pow(2, float64(combo))
			a = numerator / int(denominator)

		case BXL:
			b = b ^ literal

		case BST:
			b = combo % 8

		case JNZ:
			if a != 0 {
				pointer = literal
				continue
			}

		case BXC:
			b = b ^ c

		case OUT:
			output = append(output, combo%8)

		case BDV:
			numerator := a
			denominator := math.Pow(2, float64(combo))
			b = numerator / int(denominator)

		case CDV:
			numerator := a
			denominator := math.Pow(2, float64(combo))
			c = numerator / int(denominator)

		default:
			panic("Unknown operand")
		}
		pointer += 2
	}
	str_output := []string{}
	for _, n := range output {
		str_output = append(str_output, strconv.Itoa(n))
	}
	return strings.Join(str_output, ",")
}

func main() {

	fmt.Println(solution(10, 0, 0, []int{5, 0, 5, 1, 5, 4}))   // "0,1,2"
	fmt.Println(solution(2024, 0, 0, []int{0, 1, 5, 4, 3, 0})) // "4,2,5,6,7,7,7,7,3,1,0"
	fmt.Println(solution(729, 0, 0, []int{0, 1, 5, 4, 3, 0}))  // "4,6,3,5,6,3,5,2,1,0"

	fmt.Println(
		solution(32916674, 0, 0, []int{2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0}),
	) // "7,1,2,3,2,6,7,2,5"
}
