// fmt.Println(space_index, file_index)
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type File struct {
	index int
	size  int
}

type Files map[int]File

func parse(filename string) (Files, []File, int) {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	data := strings.Trim(string(raw_data), "\n")

	file_id := 0
	files := make(Files)
	space := []File{}
	disk_pointer := 0

	for index := 0; index < len(data); index += 2 {
		// files
		blocks_str := data[index]
		blocks, _ := strconv.Atoi(string(blocks_str))
		files[file_id] = File{disk_pointer, blocks}
		disk_pointer += blocks

		// space
		if index+1 < len(data) {
			spaces_str := data[index+1]
			spaces_size, _ := strconv.Atoi(string(spaces_str))
			space = append(space, File{disk_pointer, spaces_size})
			disk_pointer += spaces_size
		}
		file_id++
	}
	return files, space, file_id - 1
}

func solve(files Files, spaces []File, latest_content int) int {

	for content_id := latest_content; content_id >= 0; content_id-- {
		original_index := files[content_id].index
		size_to_be_moved := files[content_id].size

		for i, item := range spaces {
			index, space_size := item.index, item.size

			if index >= original_index {
				break
			}

			if space_size >= size_to_be_moved {
				// do not create free space in the place of the move file.
				// it does nothing

				files[content_id] = File{index, size_to_be_moved}

				new_space_size := space_size - size_to_be_moved
				new_space_index := index + size_to_be_moved

				if new_space_size > 0 {
					spaces[i] = File{new_space_index, new_space_size}
				} else {
					spaces = append(spaces[:i], spaces[i+1:]...)
				}
				break
			}
		}
	}

	check_sum := 0
	for file_id, item := range files {
		index, size := item.index, item.size
		check_sum += file_id * ((index+size-1)*(index+size)/2 - (index-1)*index/2)
	}
	return check_sum
}

func solution(filename string) int {
	files, spaces, latest_content := parse(filename)
	return solve(files, spaces, latest_content)
}

func main() {
	fmt.Println(solution("./example.txt")) // 2858
	fmt.Println(solution("./input.txt"))   // 6362722604045
}
