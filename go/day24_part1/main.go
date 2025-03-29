package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Input struct {
	name  string
	value int
}

type Operation struct {
	var1 string
	oper string
	var2 string
	res  string
}

func parse(filename string) (map[string]int, []Operation) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")
	inputs := make(map[string]int)

	// parse inputs
	for _, line := range strings.Split(blocks[0], "\n") {
		parts := strings.Split(line, ":")
		var_name := parts[0]
		value_str := strings.Trim(parts[1], " ")
		value, _ := strconv.Atoi(value_str)

		inputs[var_name] = value
	}

	re_opers := regexp.MustCompile(`(\w+) (\w+) (\w+) -> (\w+)`)
	operations := []Operation{}

	// parse operations
	for _, line := range strings.Split(blocks[1], "\n") {
		matches := re_opers.FindStringSubmatch(line)

		var1 := matches[1]
		oper := matches[2]
		var2 := matches[3]
		res := matches[4]

		operations = append(operations, Operation{var1, oper, var2, res})
	}

	return inputs, operations
}

func solve(inputs map[string]int, operations []Operation) int {
	results := make(map[string]int)
	for k, v := range inputs {
		results[k] = v
	}

	remaining_operations := operations
	done := NewSet[Operation]()
	var res int

	// run through operations
	for len(remaining_operations) > 0 {
		remaining_operations = []Operation{}

		for _, oper := range operations {
			if done.contains(oper) {
				continue
			}

			_, var1_in_results := results[oper.var1]
			_, var2_in_results := results[oper.var2]
			if !var1_in_results || !var2_in_results {
				remaining_operations = append(remaining_operations, oper)
				continue
			}

			switch oper.oper {
			case "AND":
				res = results[oper.var1] & results[oper.var2]
			case "OR":
				res = results[oper.var1] | results[oper.var2]
			case "XOR":
				res = results[oper.var1] ^ results[oper.var2]
			default:
				panic("Invalid operation")
			}
			results[oper.res] = res
			done.add(oper)
		}
	}

	// build binary string
	bin_str := []string{}
	for index := 50; index >= 0; index-- {
		z_index := fmt.Sprintf("z%02d", index)
		value, z_in_results := results[z_index]
		if z_in_results {
			bin_str = append(bin_str, strconv.Itoa(value))
		}
	}
	// convert 1 and 0s to a integer
	bin_digits := strings.Join(bin_str, "")
	int_value, _ := strconv.ParseInt(bin_digits, 2, 64)
	return int(int_value)
}

func solution(filename string) int {
	inputs, operations := parse(filename)
	return solve(inputs, operations)
}

func main() {
	fmt.Println(solution("./example.txt"))  // 4
	fmt.Println(solution("./example1.txt")) // 2024
	fmt.Println(solution("./input.txt"))    // 60614602965288
}
