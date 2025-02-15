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

func find(i int, parent []int) int {
	// find method for union/find/disjoint-sets
	if parent[i] == i {
		return i
	}
	return find(parent[i], parent)
}

func union(i, j int, parent []int) {
	// union method for union/find/disjoint-sets
	i_root := find(i, parent)
	j_root := find(j, parent)
	parent[i_root] = j_root
}

func are_neighbors(edge1, edge2 Point) bool {
	// determine if to edges (points) are neighbors
	row, col := edge1.row, edge1.col
	for _, new_point := range []Point{{row, col + 1}, {row, col - 1}, {row + 1, col}, {row - 1, col}} {
		if new_point == edge2 {
			return true
		}
	}
	return false
}

func get_sides(members Region) int {
	// get sides of a region
	edges := Edges{}
	for member := range members {
		row, col := member.row, member.col
		for _, step := range [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
			step_row, step_col := step[0], step[1]
			new_row := row + step_row
			new_col := col + step_col

			_, is_in_members := members[Point{new_row, new_col}]
			if !is_in_members {
				edges = append(edges, Edge{member, Point{step_row, step_col}})
			}
		}
	}
	// Create relationships for a union/find algo
	parent := []int{}
	for i := 0; i < len(edges); i++ {
		parent = append(parent, i)
	}

	for i := 0; i < len(parent); i++ {
		for j := i + 1; j < len(parent); j++ {
			if are_neighbors(edges[i].point, edges[j].point) && edges[i].dir == edges[j].dir {
				union(i, j, parent)
			}
		}
	}

	// Get disjoing sets, or sides
	sides := make(map[int]bool)
	for _, i := range parent {
		sides[find(i, parent)] = true
	}
	return len(sides)
}

func solve(garden Garden) int {
	regions := get_regions(garden)

	fence_cost := 0
	for _, members := range regions {
		fence_cost += get_sides(members) * len(members)
	}
	return fence_cost
}

func solution(filename string) int {
	garden := parse(filename)
	return solve(garden)
}

func main() {
	fmt.Println(solution("./input.txt")) // 899196
}
