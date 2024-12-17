from typing import List

ADV: int = 0
BXL: int = 1
BST: int = 2
JNZ: int = 3
BXC: int = 4
OUT: int = 5
BDV: int = 6
CDV: int = 7


def get_combo(operand: int, a: int, b: int, c: int) -> str:
    if 0 <= operand <= 3:
        return str(operand)
    elif operand == 4:
        return "a"
    elif operand == 5:
        return "b"
    elif operand == 6:
        return "c"

    return ""


def parse(a: int, b: int, c: int, program: List[int]) -> None:
    pointer: int = 0

    while 0 <= pointer < len(program):
        opcode: int = program[pointer]
        operand: int = program[pointer + 1]

        combo: str = get_combo(operand, a, b, c)
        literal: int = operand

        if opcode == ADV:
            print("ADV", combo)

        elif opcode == BXL:
            print("BXL", literal)

        elif opcode == BST:
            print("BST", combo)

        elif opcode == JNZ:
            print("JNZ", literal)

        elif opcode == BXC:
            print("BXC")

        elif opcode == OUT:
            print("OUT", combo)

        elif opcode == BDV:
            print("BDV", combo)

        elif opcode == CDV:
            print("CDV", combo)

        else:
            raise Exception("blah")

        pointer += 2


if __name__ == "__main__":
    parse(32916674, 0, 0, [2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0])
