package main

import (
	"fmt"
	"os"
	"strings"
)

func parse(filename string) Garden {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("file error")
	}

	garden := strings.Split(strings.Trim(string(data), "\n"), "\n")
	return garden
}

func get_regions(garden Garden) Regions {
	// get regions from garden
	assigned_to_zone := NewRegion()
	regions := Regions{}

	for start_row, line := range garden {
		for start_col, kind := range line {

			new_point := Point{start_row, start_col}
			if assigned_to_zone.contains(new_point) {
				continue
			}

			region := NewRegion()
			region.add(new_point)
			assigned_to_zone.add(new_point)

			// BFS init
			queue := NewQueue()
			queue.push(new_point)
			visited := NewVisitedSet()
			visited.add(new_point)

			// BFS
			for !queue.is_empty() {
				point := queue.pop()
				row, col := point.row, point.col
				if garden[row][col] != byte(kind) {
					continue
				}

				region.add(point)
				assigned_to_zone.add(point)

				for _, step := range [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
					step_row, step_col := step[0], step[1]
					new_row := row + step_row
					new_col := col + step_col

					new_point := Point{new_row, new_col}

					if 0 <= new_row && new_row < len(garden) &&
						0 <= new_col && new_col < len(garden[0]) {
						if !visited.contains(new_point) {
							queue.push(new_point)
							visited.add(new_point)
						}
					}
				}
			}
			regions = append(regions, *region)
		}
	}
	return regions
}

func get_perimeter(members Region) int {
	// get perimeter of a region
	perimeter := 0
	for member := range members {
		individual_perimeter := 4
		row, col := member.row, member.col
		for _, new_pos := range [][2]int{{row, col + 1}, {row, col - 1}, {row + 1, col}, {row - 1, col}} {
			new_row, new_col := new_pos[0], new_pos[1]
			_, is_in_members := members[Point{new_row, new_col}]
			if is_in_members {
				individual_perimeter--
			}
		}
		perimeter += individual_perimeter
	}
	return perimeter
}

func solve(garden Garden) int {
	regions := get_regions(garden)

	fence_cost := 0
	for _, members := range regions {
		fence_cost += get_perimeter(members) * len(members)
	}
	return fence_cost
}

func solution(filename string) int {
	garden := parse(filename)
	return solve(garden)
}

func main() {
	fmt.Println(solution("./input.txt")) // 1485656
}
