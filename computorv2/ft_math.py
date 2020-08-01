def ft_sqrt(num):

	if (num < 0):
		raise ValueError("math domain error")

	if num == 0:
		return 0

	x = num / 10
	y = num / x

	precision = 1e-14

	while (x - y > precision):
		x = (x + y) / 2
		y = num / x

	return x
