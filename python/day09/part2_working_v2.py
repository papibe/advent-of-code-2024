import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Match, Optional, Set, Tuple
from copy import deepcopy

def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().strip()

    # print(data)
    id_ = 0
    disk = []
    content = {}
    space = {}
    disk_pointer = 0

    for index in range(0, len(data), 2):
        blocks = data[index]
        content[id_] = (disk_pointer, int(blocks))

        disk_pointer += int(blocks)

        if index + 1 < len(data):
            space_size = data[index + 1]
            space[disk_pointer] = int(space_size)
            disk_pointer += int(space_size)

        id_ += 1

    print(f"{disk_pointer = }")

    # print(content)
    # print(space)
    latest_content = id_ - 1

    # for i in range(42):
    #     for k, v in content.items():
    #         if i == v[0]:
    #             print(str(k) * v[1], end="")
    #     if i in space:
    #         print("." * space[i], end="")
    # print()

    for content_id in range(latest_content, -1, -1):

        original_index = content[content_id][0]
        size_to_be_moved = content[content_id][1]
        # print(content_id, size_to_be_moved)

        # find first space
        # space_copy = deepcopy(space)
        # for index, space_size in space_copy.items():
        spaces_indexes = sorted(space.keys())
        # print(f"{spaces_indexes = }")
        for index in spaces_indexes:
            if index >= original_index:
                continue
            space_size = space[index]
            if space_size >= size_to_be_moved:
                # print(content_id, "moving", size_to_be_moved)
                # print("  ", index, space_size)

                space[original_index] = size_to_be_moved

                content[content_id] = (index, size_to_be_moved)

                new_space_size = space_size - size_to_be_moved
                new_space_index = index + size_to_be_moved
                del space[index]
                # print(f"{new_space_index = } {new_space_size = }")
                if new_space_size > 0:
                    space[new_space_index] = new_space_size


                break

        # print(space)
        # print(content)

        # for i in range(42):
        #     # print(f"\n{i = }\n")
        #     for k, v in content.items():
        #         if i == v[0]:
        #             print(str(k) * v[1], end="")
        #     if i in space:
        #         print("." * space[i], end="")
        # print()


    total = 0
    # content_indexes = {}
    # for k, v in content.items():
    #     content_indexes[v[0]] = (k, v[1])

    content_indexes = [v[0] for k, v in content.items()]

    disk_index = 0
    for index in content_indexes:
        # print(f"\n{i = }\n")
        for k, v in content.items():
            if index == v[0]:
                for i in range(index, index + v[1]):
                    total += k * i


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
