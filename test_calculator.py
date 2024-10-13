
from calculator import sum, mult

def test_sum():
    assert sum(2, 3) == 5
    assert sum(-1, 1) == 0
    assert sum(0, 0) == 0

def test_mult():
    assert mult(2, 3) == 6
    assert mult(1, 1) == 1
