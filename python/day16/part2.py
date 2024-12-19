from collections import defaultdict, deque, namedtuple
from typing import DefaultDict, Deque, List, Set, Tuple

START: str = "S"
END: str = "E"
WALL: str = "#"

Point = namedtuple("Point", ["row", "col"])
State = namedtuple("State", ["row", "col", "row_dir", "col_dir"])
QueueState = namedtuple("QueueState", ["row", "col", "row_dir", "col_dir", "cost"])


# def parse(filename: str) -> Tuple[List[str], int, int, int, int]:
def parse(filename: str) -> Tuple[List[str], Point, Point]:
    with open(filename, "r") as fp:
        grid: List[str] = fp.read().splitlines()

    start_row: int
    start_col: int
    end_row: int
    end_col: int

    # find start and end
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == START:
                start_row = row
                start_col = col
            elif cell == END:
                end_row = row
                end_col = col

    return grid, Point(start_row, start_col), Point(end_row, end_col)


def solve(
    grid: List[str], start_row: int, start_col: int, end_row: int, end_col: int
) -> int:

    # dijkstra's setup
    costs: DefaultDict[State, int] = defaultdict(lambda: float("inf"))  # type: ignore
    costs[State(start_row, start_col, 0, 1)] = 0
    prev: DefaultDict[State, Set[State]] = defaultdict(lambda: set())
    queue: Deque[QueueState] = deque([QueueState(start_row, start_col, 0, 1, 0)])

    # dijkstra
    while queue:
        row, col, dir_row, dir_col, cost = queue.popleft()

        for row_step, col_step in [
            (dir_row, dir_col),
            (dir_col, -dir_row),
            (-dir_col, dir_row),
        ]:
            new_row: int = row + row_step
            new_col: int = col + col_step

            if grid[new_row][new_col] == "#":
                continue

            new_cost: int
            if (row_step, col_step) == (dir_row, dir_col):
                new_cost = cost + 1
            else:
                new_row, new_col = row, col
                new_cost = cost + 1000

            if new_cost < costs[State(new_row, new_col, row_step, col_step)]:
                costs[State(new_row, new_col, row_step, col_step)] = new_cost
                prev[State(new_row, new_col, row_step, col_step)] = set(
                    [State(row, col, dir_row, dir_col)]
                )
                queue.append(QueueState(new_row, new_col, row_step, col_step, new_cost))

            elif new_cost == costs[State(new_row, new_col, row_step, col_step)]:
                prev[State(new_row, new_col, row_step, col_step)].add(
                    State(row, col, dir_row, dir_col)
                )

    # get min score to get to the end
    min_score: int = min(
        costs[State(end_row, end_col, rd, cd)]
        for rd, cd in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    )
    # get ends (pos+dir) that have min_score
    min_ends: List[State] = [
        State(end_row, end_col, rd, cd)
        for rd, cd in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if costs[State(end_row, end_col, rd, cd)] == min_score
    ]

    # reverse walk
    queue_for_path: Deque[State] = deque(min_ends)
    good_seats_positions: Set[State] = set(min_ends)

    while queue_for_path:
        end: State = queue_for_path.pop()
        for seat in prev[end]:
            if seat not in good_seats_positions:
                queue_for_path.append(seat)
                good_seats_positions.add(seat)

    # clean up seats with no direction
    good_seats: Set[Tuple[int, int]] = {(r, c) for r, c, _, _ in good_seats_positions}

    return len(good_seats)


def solution(filename: str) -> int:
    grid, (start_row, start_col), (end_row, end_col) = parse(filename)
    return solve(grid, start_row, start_col, end_row, end_col)


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 45
    print(solution("./example2.txt"))  # 64
    print(solution("./input.txt"))  # 559
