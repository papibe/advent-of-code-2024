import re


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read()

    return data


def solve(data: str) -> int:
    regex: str = r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"

    total_sum: int = 0
    enable: bool = True

    for match in re.finditer(regex, data, re.DOTALL):
        if match.group(0) == "don't()":
            enable = False

        elif match.group(0) == "do()":
            enable = True

        elif enable:
            total_sum += int(match.group(1)) * int(match.group(2))

    return total_sum


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 48
    print(solution("./input.txt"))  # 67269798
