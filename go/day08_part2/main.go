package main

import (
	"fmt"
	"os"
	"strings"
)

type Point struct {
	x int
	y int
}

type Antinode Point

func parse(filename string) (map[rune]map[Point]bool, int, int) {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	lines := strings.Split(strings.Trim(string(data), "\n"), "\n")

	rows, cols := len(lines), len(lines[0])
	antenas := make(map[rune]map[Point]bool)

	for y, line := range lines {
		for x, char := range line {
			if char != '.' && char != '#' { // support example data
				_, ok := antenas[char]
				if !ok {
					antenas[char] = make(map[Point]bool)
				}
				antenas[char][Point{x, y}] = true
			}
		}
	}

	return antenas, rows, cols
}

func solve(antenas map[rune]map[Point]bool, rows, cols int) int {
	antinodes := make(map[Antinode]bool)

	for _, positions := range antenas {

		// convert map into slice to build combinations
		antenas_slice := []Point{}
		for point := range positions {
			antenas_slice = append(antenas_slice, point)
		}

		// create combinations of length 2
		for i := 0; i < len(antenas_slice); i++ {
			for j := i + 1; j < len(antenas_slice); j++ {
				antena1 := antenas_slice[i]
				antena2 := antenas_slice[j]
				antinodes[Antinode(antena1)] = true

				delta_x := antena1.x - antena2.x
				delta_y := antena1.y - antena2.y

				// go through the line formed by antena1 and antena2
				for _, delta := range [][2]int{{delta_x, delta_y}, {-delta_x, -delta_y}} {
					dx, dy := delta[0], delta[1]
					antinode := Antinode{antena1.x + dx, antena1.y + dy}

					for 0 <= antinode.x && antinode.x < rows &&
						0 <= antinode.y && antinode.y < cols {

						antinodes[antinode] = true
						antinode = Antinode{antinode.x + dx, antinode.y + dy}
					}
				}
			}
		}
	}
	return len(antinodes)
}

func solution(filename string) int {
	antenas, rows, cols := parse(filename)
	return solve(antenas, rows, cols)
}

func main() {
	fmt.Println(solution("./input.txt")) // 1249
}
