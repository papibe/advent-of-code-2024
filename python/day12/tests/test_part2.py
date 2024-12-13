import pytest

from part2 import solution


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("./example1.txt", 80),
        ("./example2.txt", 436),
        ("./example4.txt", 236),
        ("./example5.txt", 368),
        ("./example3.txt", 1206),
    ],
)
def test_part2(filename: str, expected: int) -> None:
    result: int = solution(filename)
    assert result == expected, f"got {result}, needs {expected}"
