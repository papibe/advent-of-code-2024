package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"sort"
	"strings"
)

const ALL_GOOD = -1

type Operation struct {
	var1 string
	oper string
	var2 string
	res  string
}

type MOperation struct {
	oper  Operation
	index int
}

func parse(filename string) []Operation {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	// skip parsing inputs in blocks[0]

	// parse operations
	regex := regexp.MustCompile(`(\w+) (\w+) (\w+) -> (\w+)`)
	operations := []Operation{}

	for _, line := range strings.Split(blocks[1], "\n") {
		matches := regex.FindStringSubmatch(line)
		var1 := matches[1]
		oper := matches[2]
		var2 := matches[3]
		res := matches[4]

		operations = append(operations, Operation{var1, oper, var2, res})
	}

	return operations
}

func get_value(inputs map[string]int, var_name string) int {
	// collects values of a variable and converts them into an integer
	value := 0
	for index := range 46 {
		var_digit_name := fmt.Sprintf("%s%02d", var_name, index)
		value += inputs[var_digit_name] * int(math.Pow(2.0, float64(index)))
	}
	return value
}

func run_operations(inputs map[string]int, operations []Operation) int {
	// run through the list of operations

	// set initial values from inputs
	results := make(map[string]int)
	for k, v := range inputs {
		results[k] = v
	}

	// run through operations
	var r int
	for {
		changed := false

		for _, o := range operations {

			_, var1_in_results := results[o.var1]
			_, var2_in_results := results[o.var2]
			_, res_in_results := results[o.res]

			if var1_in_results && var2_in_results && !res_in_results {
				switch o.oper {
				case "AND":
					r = results[o.var1] & results[o.var2]
				case "OR":
					r = results[o.var1] | results[o.var2]
				case "XOR":
					r = results[o.var1] ^ results[o.var2]
				default:
					panic("Invalid operation")
				}
				results[o.res] = r
				changed = true
			}
		}
		if !changed {
			break
		}
	}
	return get_value(results, "z")
}

func get_affected_operations(operations []Operation, index int) []MOperation {
	// get set of operations that potentially impact the value at position `index`

	a_operations := NewSet[MOperation]()

	initial_results := NewSet[string]()

	previous_z := fmt.Sprintf("z%02d", index-1)
	current_z := fmt.Sprintf("z%02d", index)
	next_z := fmt.Sprintf("z%02d", index+1)

	initial_results.add(previous_z)
	initial_results.add(current_z)
	initial_results.add(next_z)

	for index, o := range operations {
		if initial_results.contains(o.res) {
			a_operations.add(MOperation{o, index})
		}
	}

	vars := NewSet[string]()
	for o := range a_operations.elements {
		vars.add(o.oper.var1)
		vars.add(o.oper.var2)
	}

	for index, o := range operations {
		if vars.contains(o.var1) || vars.contains(o.var2) || vars.contains(o.res) {
			a_operations.add(MOperation{o, index})

		}
	}

	for o := range a_operations.elements {
		vars.add(o.oper.var1)
		vars.add(o.oper.var2)
		vars.add(o.oper.res)
	}

	for index, o := range operations {
		if vars.contains(o.var1) || vars.contains(o.var2) || vars.contains(o.res) {
			a_operations.add(MOperation{o, index})
		}
	}

	return a_operations.list_of_elements()
}

func test(x, y int, operations []Operation) bool {
	// check if run operations with x and y is equal to x+y
	inputs := make(map[string]int)
	for index := range 45 {
		x_digit := x & (1 << index) >> index
		y_digit := y & (1 << index) >> index

		x_key := fmt.Sprintf("x%02d", index)
		y_key := fmt.Sprintf("y%02d", index)

		inputs[x_key] = x_digit
		inputs[y_key] = y_digit
	}

	z := run_operations(inputs, operations)

	return (x+y == z)
}

func get_error_at_index(operations []Operation, min_index, max_index int) int {
	// Try 4 tests to check if operations return proper value on a index's range
	for i := min_index; i < max_index; i++ {
		tests_ok := true
		power_of_2 := 1 << i

		tests_ok = tests_ok && test(power_of_2, 0, operations)
		tests_ok = tests_ok && test(0, power_of_2, operations)
		tests_ok = tests_ok && test(power_of_2, power_of_2, operations)

		just_ones := (1 << i) - 1
		tests_ok = tests_ok && test(just_ones, 1, operations)

		if !tests_ok {
			return i
		}
	}
	return -1
}

func combinations(a_operations []MOperation) [][2]MOperation {
	// get all combinations of size 2 of a list of objects
	combos := [][2]MOperation{}

	for i := 0; i < len(a_operations); i++ {
		for j := i + 1; j < len(a_operations); j++ {
			combos = append(combos, [2]MOperation{a_operations[i], a_operations[j]})
		}
	}
	return combos
}

func solve(operations []Operation) string {
	output := []string{}

	index := get_error_at_index(operations, 0, 45)
	for index != ALL_GOOD {
		fmt.Println("Problem detected at index", index)

		a_operations := get_affected_operations(operations, index)
		fmt.Println("Operations considered for swapping:", len(a_operations))

		for _, combo := range combinations(a_operations) {
			o1, o2 := combo[0], combo[1]

			// swap results
			operations[o1.index].res = o2.oper.res
			operations[o2.index].res = o1.oper.res

			if get_error_at_index(operations, index-1, index+3) == ALL_GOOD {
				fmt.Println("fixing by swapping:")
				fmt.Println("  ", o1)
				fmt.Println("  ", o2)
				fmt.Println()
				output = append(output, o1.oper.res)
				output = append(output, o2.oper.res)
				break
			}
			// restore results
			operations[o1.index].res = o1.oper.res
			operations[o2.index].res = o2.oper.res
		}
		index = get_error_at_index(operations, index, 45)
	}
	sort.Strings(output)
	return strings.Join(output, ",")
}

func solution(filename string) string {
	operations := parse(filename)
	return solve(operations)
}

func main() {
	fmt.Println(solution("./input.txt")) // "cgr,hpc,hwk,qmd,tnt,z06,z31,z37"
}
