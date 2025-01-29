package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) (map[string]map[string]bool, [][]string) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}

	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	// parse rules
	rules := make(map[string]map[string]bool)
	for _, line := range strings.Split(blocks[0], "\n") {
		pages := strings.Split(line, "|")
		_, ok := rules[pages[0]]
		if !ok {
			rules[pages[0]] = make(map[string]bool)
		}
		rules[pages[0]][pages[1]] = true
	}

	// parse updates
	updates := [][]string{}
	for _, line := range strings.Split(blocks[1], "\n") {
		updates = append(updates, strings.Split(line, ","))
	}
	return rules, updates
}

func get_unorder(update []string, rules map[string]map[string]bool) (int, int, bool) {
	for i := len(update) - 1; i > -1; i-- {
		for j := i - 1; j > -1; j-- {
			_, update_i_in_rules := rules[update[i]]
			_, update_j_in_rules_i := rules[update[i]][update[j]]

			if update_i_in_rules && update_j_in_rules_i {
				return i, j, false
			}
		}
	}
	return 0, 0, true
}

func solve(rules map[string]map[string]bool, updates [][]string) int {
	middle_sum := 0
	for _, update := range updates {
		i, j, is_good := get_unorder(update, rules)
		if !is_good {
			for !is_good {
				update[i], update[j] = update[j], update[i]
				i, j, is_good = get_unorder(update, rules)
			}
			mid_value, _ := strconv.Atoi(update[len(update)/2])
			middle_sum += mid_value
		}
	}
	return middle_sum
}

func solution(filename string) int {
	rules, updates := parse(filename)
	return solve(rules, updates)
}

func main() {
	fmt.Println(solution("./example.txt")) // 123
	fmt.Println(solution("./input.txt"))   // 4598
}
