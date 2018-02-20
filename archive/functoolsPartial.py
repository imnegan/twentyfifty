from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

def test_partials():
    assert square(3) == 4
    assert cube(2) == 8
	
test_partials()