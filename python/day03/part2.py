import re


def parse(filename: str) -> str:
    with open(filename, "r") as fp:
        data: str = fp.read()

    return data


def solve(data: str) -> int:
    # regular expressions
    re_mul: str = r"mul\((\d+),(\d+)\)"
    re_do: str = r"do\(\)"
    re_dont: str = "don't\(\)"

    # list of matches and its indices
    muls = [
        (match.start(), match.group(1), match.group(2))
        for match in re.finditer(re_mul, data, re.DOTALL)
    ]
    dos = [
        (match.start(), match.group()) for match in re.finditer(re_do, data, re.DOTALL)
    ]
    donts = [
        (match.start(), match.group())
        for match in re.finditer(re_dont, data, re.DOTALL)
    ]

    all_matches = muls + dos + donts
    all_matches.sort()

    total_sum: int = 0
    enable: bool = True

    for match in all_matches:
        # multiplication
        if len(match) == 3 and enable:
            total_sum += int(match[1]) * int(match[2])

        # dont match
        elif match[1] == "don't()":
            enable = False

        # do match
        elif match[1] == "do()":
            enable = True

    return total_sum


def solution(filename: str) -> int:

    data: str = parse(filename)
    return solve(data)


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 48
    print(solution("./input.txt"))  # 67269798
