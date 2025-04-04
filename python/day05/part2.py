from typing import Dict, List, Set, Tuple

Rules = Dict[str, Set[str]]
Update = List[str]
Updates = List[Update]


def parse(filename: str) -> Tuple[Rules, Updates]:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    # parse rules
    rules: Rules = {}
    for line in blocks[0].splitlines():
        pages = line.split("|")
        if pages[0] not in rules:
            rules[pages[0]] = set()
        rules[pages[0]].add(pages[1])

    # parse updates
    updates: Updates = []
    for line in blocks[1].splitlines():
        updates.append([n for n in line.split(",")])

    return rules, updates


def get_unorder(update: Update, rules: Rules) -> Tuple[int, int, bool]:
    """check if a printer update is correctly ordered"""
    for i in range(len(update) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            if update[i] in rules and update[j] in rules[update[i]]:
                return i, j, False
    return 0, 0, True


def solve(rules: Rules, updates: List[List[str]]) -> int:
    middle_sum: int = 0
    for update in updates:
        i, j, is_good = get_unorder(update, rules)
        if not is_good:
            while not is_good:
                update[i], update[j] = update[j], update[i]
                i, j, is_good = get_unorder(update, rules)

            middle_sum += int(update[len(update) // 2])

    return middle_sum


def solution(filename: str) -> int:
    rules, updates = parse(filename)
    return solve(rules, updates)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 123
    print(solution("./input.txt"))  # 4598
