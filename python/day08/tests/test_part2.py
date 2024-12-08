import pytest

from part2 import solution


@pytest.mark.parametrize(
    "input_file,expected",
    [
        ("example5.txt", 9),
        ("example4.txt", 34),
    ],
)
def test_part2(input_file: str, expected: int) -> None:
    result: int = solution(input_file)
    assert result == expected, f"got {result}, needs {expected}"
