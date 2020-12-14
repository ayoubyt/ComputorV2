import math
from .types import Real

def my_sqrt(num):

	if (num < 0):
		raise ValueError("math domain error")

	if num == 0:
		return 0

	x = num
	y = num / x

	precision = 1e-14

	while (x - y > precision):
		x = (x + y) / 2
		y = num / x

	return x


def ft_sqrt(x: Real):
    return Real(my_sqrt(x.re))


def ft_max(a: Real, b: Real):
    return (a if a > b else b)


def ft_min(a: Real, b: Real):
    return (a if a < b else b)
