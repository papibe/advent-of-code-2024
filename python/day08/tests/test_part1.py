import pytest

from part1 import solution


@pytest.mark.parametrize(
    "input_file,expected",
    [
        ("example1.txt", 2),
        ("example2.txt", 4),
        ("example3.txt", 4),
        ("example4.txt", 14),
    ],
)
def test_part1(input_file: str, expected: int) -> None:
    result: int = solution(input_file)
    assert result == expected, f"got {result}, needs {expected}"
