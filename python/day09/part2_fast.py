import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple, NamedTuple
from copy import deepcopy

class File(NamedTuple):
    index: int
    size: int


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().strip()

    file_id = 0
    content: Dict[int, File] = {}
    space: Dict[int, int] = {}
    disk_pointer = 0

    for index in range(0, len(data), 2):
        # files
        blocks = int(data[index])
        content[file_id] = File(disk_pointer, blocks)
        disk_pointer += blocks

        # spaces
        if index + 1 < len(data):
            space_size = int(data[index + 1])
            space[disk_pointer] = space_size
            disk_pointer += space_size

        file_id += 1


    latest_content = file_id - 1

    for content_id in range(latest_content, -1, -1):

        original_index = content[content_id].index
        size_to_be_moved = content[content_id].size

        spaces_indexes = sorted(space.keys())

        for index in spaces_indexes:

            if index >= original_index:
                continue
            space_size = space[index]

            if space_size >= size_to_be_moved:

                space[original_index] = size_to_be_moved

                content[content_id] = (index, size_to_be_moved)

                new_space_size = space_size - size_to_be_moved
                new_space_index = index + size_to_be_moved
                del space[index]

                if new_space_size > 0:
                    space[new_space_index] = new_space_size

                break

        # for i in range(42):
        #     # print(f"\n{i = }\n")
        #     for k, v in content.items():
        #         if i == v[0]:
        #             print(str(k) * v[1], end="")
        #     if i in space:
        #         print("." * space[i], end="")
        # print()


    total = 0
    content_indexes = {}
    for k, v in content.items():
        content_indexes[v[0]] = (k, v[1])


    disk_index = 0
    for index, item in content_indexes.items():
        k, v = item

        # for i in range(index, index + v):
        #     total += k * i

        # sum_ = (
        #     (index + v - 1) * (index + v) // 2
        #     - (index - 1) * index // 2
        # )
        # total += k * sum_

        total +=  k * (
            (index + v - 1) * (index + v) // 2
            - (index - 1) * index // 2
        )
        # total += k * sum_



    print(f"{total = }")
    assert total == 6362722604045

    return data


def solve(data: List[str]) -> int:
    total_sum: int = 0

    for row in data:
        pass

    return total_sum


def solution(filename: str) -> int:
    data: List[str] = parse(filename)
    return solve(data)


if __name__ == "__main__":
    # print(solution("./example2.txt"))  # 0
    # print(solution("./example.txt"))  # 0
    result = solution("./input.txt")  # 6362722604045
    print(result)  # 0
