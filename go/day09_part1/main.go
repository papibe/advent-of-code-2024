package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parse(filename string) []string {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	file_id := 0
	disk := []string{}
	data := strings.Trim(string(raw_data), "\n")

	for index := 0; index < len(data); index += 2 {
		// files
		blocks_str := data[index]
		blocks, _ := strconv.Atoi(string(blocks_str))
		for range blocks {
			disk = append(disk, strconv.Itoa(file_id))
		}

		// spaces
		if index+1 < len(data) {
			spaces_str := data[index+1]
			spaces, _ := strconv.Atoi(string(spaces_str))
			for range spaces {
				disk = append(disk, ".")
			}
		}
		file_id++
	}
	return disk
}

func get_next_space(disk []string, start_index int) int {
	// get the next space starting from the left
	for index := start_index; index < len(disk); index++ {
		if disk[index] == "." {
			return index
		}
	}
	return -1
}

func get_next_file(disk []string, start_index int) int {
	// get the next file starting from the right
	for index := start_index; index >= 0; index-- {
		if disk[index] != "." {
			return index
		}
	}
	return -1
}

func solve(disk []string) int {
	space_index := get_next_space(disk, 0)
	file_index := get_next_file(disk, len(disk)-1)

	for space_index < file_index {
		disk[space_index], disk[file_index] = disk[file_index], disk[space_index]

		// get next spaces and files indexes
		space_index = get_next_space(disk, space_index)
		file_index = get_next_file(disk, file_index)
	}

	check_sum := 0
	for block_index, file_id_str := range disk {
		if file_id_str == "." {
			break
		}
		file_id, _ := strconv.Atoi(file_id_str)
		check_sum += block_index * file_id
	}
	return check_sum
}

func solution(filename string) int {
	disk := parse(filename)
	return solve(disk)
}

func main() {
	fmt.Println(solution("./example.txt")) // 1928
	fmt.Println(solution("./input.txt"))   // 6337921897505
}
