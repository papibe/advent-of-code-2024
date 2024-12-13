import re
from dataclasses import dataclass
from typing import List, Match, Optional


@dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int


def parse(filename: str) -> List[Machine]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    button_regex: str = r"Button (\w): X\+(\d+), Y\+(\d+)"
    price_regex: str = r"Prize: X=(\d+), Y=(\d+)"

    machines: List[Machine] = []

    for machine in blocks:
        lines: List[str] = machine.splitlines()
        a_button: Optional[Match[str]] = re.match(button_regex, lines[0])
        b_button: Optional[Match[str]] = re.match(button_regex, lines[1])
        price: Optional[Match[str]] = re.match(price_regex, lines[2])

        if a_button and b_button and price:
            machines.append(
                Machine(
                    ax=int(a_button.group(2)),
                    ay=int(a_button.group(3)),
                    bx=int(b_button.group(2)),
                    by=int(b_button.group(3)),
                    px=int(price.group(1)) + 10000000000000,
                    py=int(price.group(2)) + 10000000000000,
                )
            )
    return machines


def solve(machines: List[Machine]) -> int:
    total_cost: int = 0
    for m in machines:
        a_divisor: int = (m.ay * m.bx) - (m.by * m.ax)
        a_dividend: int = (m.bx * m.py) - (m.px * m.by)

        # skip non integer solution for a
        if a_divisor == 0 or a_dividend % a_divisor != 0:
            continue

        a: int = a_dividend // a_divisor

        b_divisor: int = m.bx
        b_dividend: int = m.px - (m.ax * a)

        # skip non integer solutions for b
        if b_divisor == 0 or b_dividend % b_divisor != 0:
            continue

        b: int = b_dividend // b_divisor

        total_cost += (a * 3) + b

    return total_cost


def solution(filename: str) -> int:
    machines: List[Machine] = parse(filename)
    return solve(machines)


if __name__ == "__main__":
    print(solution("./input.txt"))  # 106228669504887
