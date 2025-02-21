package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Machine struct {
	ax int
	ay int
	bx int
	by int
	px int
	py int
}

func parse(filename string) []Machine {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	blocks := strings.Split(strings.Trim(string(data), "\n"), "\n\n")

	button_regex := regexp.MustCompile(`Button (\w): X\+(\d+), Y\+(\d+)`)
	price_regex := regexp.MustCompile(`Prize: X=(\d+), Y=(\d+)`)

	machines := []Machine{}

	for _, machine := range blocks {
		lines := strings.Split(machine, "\n")
		a_button := button_regex.FindStringSubmatch(lines[0])
		b_button := button_regex.FindStringSubmatch(lines[1])
		price := price_regex.FindStringSubmatch(lines[2])

		ax, _ := strconv.Atoi(a_button[2])
		ay, _ := strconv.Atoi(a_button[3])
		bx, _ := strconv.Atoi(b_button[2])
		by, _ := strconv.Atoi(b_button[3])
		px, _ := strconv.Atoi(price[1])
		py, _ := strconv.Atoi(price[2])

		// part 2 adjustment
		px += 10000000000000
		py += 10000000000000

		machines = append(machines, Machine{ax, ay, bx, by, px, py})

	}
	return machines
}

func solve(machines []Machine) int {
	total_cost := 0
	for _, m := range machines {
		a_divisor := (m.ay * m.bx) - (m.by * m.ax)
		a_dividend := (m.bx * m.py) - (m.px * m.by)

		// skip non integer solution for a
		if a_divisor == 0 || a_dividend%a_divisor != 0 {
			continue
		}

		a := a_dividend / a_divisor

		b_divisor := m.bx
		b_dividend := m.px - (m.ax * a)

		// skip non integer solutions for b
		if b_divisor == 0 || b_dividend%b_divisor != 0 {
			continue
		}
		b := b_dividend / b_divisor

		total_cost += (a * 3) + b
	}
	return total_cost
}

func solution(filename string) int {
	machines := parse(filename)
	return solve(machines)

}

func main() {
	fmt.Println(solution("./input.txt")) // 106228669504887
}
