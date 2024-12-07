from typing import List, Tuple

Operands = List[int]
Equations = List[Tuple[int, Operands]]


def parse(filename: str) -> Equations:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    equations = []
    for line in data:
        # get test_value
        test_str, other_values = line.split(":")
        test_value: int = int(test_str)

        # get values or operands
        values = other_values.strip().split(" ")
        operands: Operands = [int(value) for value in values]

        equations.append((test_value, operands))

    return equations


def eq_is_possible(test_value: int, operands: Operands, current_value: int) -> bool:
    """DFS like function that evaluate the equation"""
    if not operands:
        return test_value == current_value

    if current_value > test_value:
        return False

    plus: bool = eq_is_possible(test_value, operands[1:], current_value * operands[0])
    mul: bool = eq_is_possible(test_value, operands[1:], current_value + operands[0])
    concat: bool = eq_is_possible(
        test_value, operands[1:], int(str(current_value) + str(operands[0]))
    )

    return plus or mul or concat


def solve(equations: Equations) -> int:
    sum_of_tests: int = 0
    for test_value, operands in equations:
        if eq_is_possible(test_value, operands[1:], operands[0]):
            sum_of_tests += test_value

    return sum_of_tests


def solution(filename: str) -> int:
    equations: Equations = parse(filename)
    return solve(equations)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 11387
    print(solution("./input.txt"))  # 581941094529163
