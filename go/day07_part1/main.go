package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Equation struct {
	value    int
	operands []int
}

func parse(filename string) []Equation {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	equations := []Equation{}
	for _, line := range lines {
		// get test value
		line_parts := strings.Split(line, ":")
		test_str, other_values := line_parts[0], line_parts[1]
		test_value, _ := strconv.Atoi(test_str)

		// get values or operands
		other_values_parts := strings.Split(strings.TrimSpace(other_values), " ")
		operands := []int{}
		for _, value_str := range other_values_parts {
			value, _ := strconv.Atoi(value_str)
			operands = append(operands, value)
		}

		equations = append(equations, Equation{test_value, operands})
	}

	return equations
}

func eq_is_possible(test_value int, operands []int, current_value int) bool {
	// DFS-lime function that evaluate equation
	if len(operands) == 0 {
		return (test_value == current_value)
	}

	if current_value > test_value {
		return false
	}

	plus_ok := eq_is_possible(test_value, operands[1:], current_value*operands[0])
	mul_ok := eq_is_possible(test_value, operands[1:], current_value+operands[0])

	return plus_ok || mul_ok
}

func solve(equations []Equation) int {
	sum_of_tests := 0

	for _, equation := range equations {
		if eq_is_possible(equation.value, equation.operands[1:], equation.operands[0]) {
			sum_of_tests += equation.value
		}
	}
	return sum_of_tests
}

func solution(filename string) int {
	equations := parse(filename)
	return solve(equations)
}

func main() {
	fmt.Println(solution("./example.txt")) // 3749
	fmt.Println(solution("./input.txt"))   // 21572148763543
}
