from typing import List


def dfs(program: List[int], index: int, value: int) -> int:
    """reverse enginieered from program.txt"""

    if index < 0:
        return value

    a: int
    b: int
    c: int
    output: int
    for octal_digit in range(8):
        a = (value << 3) + octal_digit
        b = a % 8
        b = b ^ 1
        c = a >> b
        b = b ^ 4
        b = b ^ c
        output = b % 8

        if output == program[index]:
            next_value = dfs(program, index - 1, a)
            if next_value != -1:
                return next_value

    return -1


def solution(program: List[int]) -> int:
    return dfs(program=program, index=len(program) - 1, value=0)


if __name__ == "__main__":
    print(solution([2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0]))  # 202356708354602
