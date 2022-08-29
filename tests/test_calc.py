from models.calculator import Calculator


def test_add():
    calc = Calculator(5, 7)
    assert calc.add() == 5 + 7


def test_sub():
    calc = Calculator(5, 7)
    assert calc.subtract() == 5 - 7


def test_mul():
    calc = Calculator(5, 7)
    assert calc.multiply() == 5 * 7


def test_div():
    calc = Calculator(5, 7)
    assert calc.divide() == 5 / 7


def test_mul_or_add_is_mul():
    calc = Calculator(1, 2)
    assert calc.multiply_or_add() == 1 * 2


def test_mul_or_add_is_add():
    calc = Calculator(2, 1)
    assert calc.multiply_or_add() == 1 + 2
