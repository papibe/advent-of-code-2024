from typing import List

Report = List[int]


def is_valid(report: Report) -> bool:
    """Determine if a report is valid"""

    if report[0] == report[1]:
        return False

    if report[0] < report[1]:
        decreasing = True
    else:
        decreasing = False

    for i in range(len(report) - 1):
        current = report[i]
        next_ = report[i + 1]

        if decreasing and current > next_:
            return False

        if not decreasing and current < next_:
            return False

        if not (1 <= abs(current - next_) <= 3):
            return False

    return True


def parse(filename: str) -> List[Report]:
    """Parse input file into a list of reports"""
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    reports: List[Report] = []

    for line in data:
        numbers = line.split()
        reports.append([int(n) for n in numbers])

    return reports


def solve(reports: List[Report]) -> int:
    valid_reports: int = 0

    for report in reports:

        # remove 1 level
        for index in range(len(report)):
            simple_report = report.copy()
            simple_report.pop(index)

            if is_valid(simple_report):
                valid_reports += 1
                break

    return valid_reports


def solution(filename: str) -> int:
    reports: List[Report] = parse(filename)
    return solve(reports)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 4
    print(solution("./input.txt"))  # 528
