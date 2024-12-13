import pytest

from part1 import solution


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("./example1.txt", 140),
        ("./example2.txt", 772),
        ("./example3.txt", 1930),
    ],
)
def test_part1(filename: str, expected: int) -> None:
    result: int = solution(filename)
    assert result == expected, f"got {result}, needs {expected}"
