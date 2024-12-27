from typing import List

ADV: int = 0
BXL: int = 1
BST: int = 2
JNZ: int = 3
BXC: int = 4
OUT: int = 5
BDV: int = 6
CDV: int = 7


def get_combo(operand: int, a: int, b: int, c: int) -> int:
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c

    return -1


def solution(a: int, b: int, c: int, program: List[int]) -> str:
    pointer: int = 0
    output: List[int] = []

    while 0 <= pointer < len(program):
        opcode: int = program[pointer]
        operand: int = program[pointer + 1]

        combo: int = get_combo(operand, a, b, c)
        literal: int = operand

        if opcode == ADV:
            numerator: int = a
            denominator: int = 2**combo
            a = numerator // denominator

        elif opcode == BXL:
            b = b ^ literal

        elif opcode == BST:
            b = combo % 8

        elif opcode == JNZ:
            if a != 0:
                pointer = literal
                continue

        elif opcode == BXC:
            b = b ^ c

        elif opcode == OUT:
            output.append(combo % 8)

        elif opcode == BDV:
            numerator = a
            denominator = 2**combo
            b = numerator // denominator

        elif opcode == CDV:
            numerator = a
            denominator = 2**combo
            c = numerator // denominator

        else:
            raise Exception("blah")

        pointer += 2

    return ",".join([str(n) for n in output])


if __name__ == "__main__":
    assert solution(10, 0, 0, [5, 0, 5, 1, 5, 4]) == "0,1,2"
    assert solution(2024, 0, 0, [0, 1, 5, 4, 3, 0]) == "4,2,5,6,7,7,7,7,3,1,0"
    assert solution(729, 0, 0, [0, 1, 5, 4, 3, 0]) == "4,6,3,5,6,3,5,2,1,0"

    print(
        solution(32916674, 0, 0, [2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0])
    )  # "7,1,2,3,2,6,7,2,5"
