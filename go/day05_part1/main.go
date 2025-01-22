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

func update_is_good(update []string, rules map[string]map[string]bool) bool {
	for i := len(update) - 1; i > -1; i-- {
		for j := i - 1; j > -1; j-- {
			_, update_i_in_rules := rules[update[i]]
			_, update_j_in_rules_i := rules[update[i]][update[j]]

			if update_i_in_rules && update_j_in_rules_i {
				return false
			}
		}
	}
	return true
}

func solve(rules map[string]map[string]bool, updates [][]string) int {
	middle_sum := 0
	for _, update := range updates {
		if update_is_good(update, rules) {
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
	fmt.Println(solution("./example.txt")) // 143
	fmt.Println(solution("./input.txt"))   // 5452
}
