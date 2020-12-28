from .polynomial import Polynomial
from ...ft_math import my_sqrt
class D2plynominal(Polynomial):

	"""
		2d Polynomial represents a second degree Polynomial
		d2Polynominal([c, b, a]) when a, b ,c represents the coefficient of
		the Polynomial a * x^2 + b * x + c
	"""

	def __init__(self, coefs):
		super().__init__(coefs)
		#print(coefs)
		if len(coefs) != 3:
			raise self.PolynominalError("3 and only 3 coeficients are required")
		c, b, a = coefs
		self.delta = b * b - 4 * a * c
		self.roots = self._get_roots()

	def solve(self):
		res = ""
		res += (str(self) + " = 0\n")
		res += ("delta : %f" % self.delta) + "\n"
		if (self.delta > 0):
			res += ("delta is positive, so there are two real solutions :\n")
			res += ("x1 = %f" % self.roots[0]) + " \n"
			res += ("x2 = %f" % self.roots[1]) + " \n"
		elif (self.delta == 0):
			res += ("delta iequal to 0, so there are one real solution :\n")
			res += ("x = %f" % self.roots[0]) + "\n"
		else:
			res += ("delta is positive, so there are two complex solutions :\n")
			res += ("z1 = %f + %fi" % (self.roots[0][0], self.roots[0][1])) + "\n"
			res += ("z2 = %f + %fi" % (self.roots[1][0], self.roots[1][1]))
		return res


	@classmethod
	def fromexpr(cls, expr):
		result = Polynomial.fromexpr(expr)
		if (result.deg != 2):
			raise cls.PolynominalError(f"affecting polynomial with deg {result.deg} to deg two polynomial")
		else:
			return cls(result.coefs)
		#print(Error)


	def _get_roots(self):
		"""
			function to get polynomial roolts
		"""
		a = b = 0
		if (self.deg > 1):
			_, b, a = self.coefs
		if (self.delta > 0):
			return (-b + my_sqrt(self.delta)) / (2 * a), (-b - my_sqrt(self.delta)) / (2 * a)
		elif (self.delta == 0):
			return [-b / (2 * a)]
		else:
			d =my_sqrt(-self.delta)
			return (-b/(2*a), -d/(2*a)), (-b/(2*a), d/(2*a))

