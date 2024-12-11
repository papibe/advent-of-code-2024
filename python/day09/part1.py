from typing import List


def parse(filename: str) -> List[str]:
    with open(filename, "r") as fp:
        data: str = fp.read().strip()

    file_id: int = 0
    disk: List[str] = []

    for index in range(0, len(data), 2):
        # files
        blocks: str = data[index]
        for _ in range(int(blocks)):
            disk.append(str(file_id))

        # spaces
        if index + 1 < len(data):
            spaces: str = data[index + 1]
            for _ in range(int(spaces)):
                disk.append(".")

        file_id += 1

    return disk


def get_next_space(disk: List[str], start_index: int) -> int:
    """get the next space starting from the left"""
    for index in range(start_index, len(disk)):
        if disk[index] == ".":
            return index
    return -1  # silly mypy


def get_next_file(disk: List[str], start_index: int) -> int:
    """get the next file starting from the right"""
    for index in range(start_index, -1, -1):
        if disk[index] != ".":
            return index
    return -1  # silly mypy


def solve(disk: List[str]) -> int:
    space_index = get_next_space(disk, start_index=0)
    file_index = get_next_file(disk, start_index=len(disk) - 1)

    while space_index < file_index:
        disk[space_index], disk[file_index] = disk[file_index], disk[space_index]

        # get next space and file indexes
        space_index = get_next_space(disk, start_index=space_index)
        file_index = get_next_file(disk, start_index=file_index)

    check_sum: int = 0
    for block_index, file_id in enumerate(disk):
        if file_id == ".":
            break
        check_sum += block_index * int(file_id)

    return check_sum


def solution(filename: str) -> int:
    disk: List[str] = parse(filename)
    return solve(disk)


if __name__ == "__main__":
    # print(solution("./example2.txt"))  # 0
    print(solution("./example1.txt"))  # 1928
    print(solution("./input.txt"))  # 6337921897505
