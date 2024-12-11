from collections import namedtuple
from typing import Dict, List, Tuple

File = namedtuple("File", ["index", "size"])
# File = Tuple[int, int]
Files = Dict[int, File]
Space = List[File]


def parse(filename: str) -> Tuple[Files, Space, int]:
    with open(filename, "r") as fp:
        data: str = fp.read().strip()

    file_id = 0
    files: Files = {}
    space: Space = []
    disk_pointer = 0

    for index in range(0, len(data), 2):
        # files
        blocks = int(data[index])
        files[file_id] = File(disk_pointer, blocks)
        disk_pointer += blocks

        # spaces
        if index + 1 < len(data):
            space_size = int(data[index + 1])
            space.append(File(disk_pointer, space_size))
            disk_pointer += space_size

        file_id += 1

    return files, space, file_id - 1


def solve(files: Files, spaces: Space, latest_content: int) -> int:
    for content_id in range(latest_content, -1, -1):

        original_index: int = files[content_id].index
        size_to_be_moved: int = files[content_id].size

        for i, (index, space_size) in enumerate(spaces):
            if index >= original_index:
                break

            if space_size >= size_to_be_moved:

                # do not create free space in the place of the move file.
                # it does nothing

                files[content_id] = File(index, size_to_be_moved)

                new_space_size = space_size - size_to_be_moved
                new_space_index = index + size_to_be_moved

                if new_space_size > 0:
                    spaces[i] = File(new_space_index, new_space_size)
                else:
                    spaces.pop(i)

                break

    checksum: int = 0
    for file_id, (index, size) in files.items():
        checksum += file_id * (
            (index + size - 1) * (index + size) // 2 - (index - 1) * index // 2
        )

    return checksum


def solution(filename: str) -> int:
    content, space, latest_content = parse(filename)
    return solve(content, space, latest_content)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 2858
    print(solution("./input.txt"))  # 6362722604045
