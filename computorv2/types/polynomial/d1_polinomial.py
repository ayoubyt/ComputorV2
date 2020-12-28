from .polynomial import Polynomial

class D1plynominal(Polynomial):

	"""
		1d Polynomial represents a first degree Polynomial
		D1plynominal([b, a]) when a, b  represents the coefficient of
		the Polynomial a * x + b
	"""

	def __init__(self, coefs):
		super().__init__(coefs)
		#print(coefs)
		if len(coefs) != 2:
			raise self.PolynominalError("2 and only 2 coeficients are required")

	def solve(self):
		res = ""
		b, a = self.coefs
		res += (str(self) + "= 0\n")
		res += ("a first degree equation with one solution :") + "\n"
		res += ("x = %f" % (-b / a))
		return res



	@classmethod
	def fromexpr(cls, expr):
		result = Polynomial.fromexpr(expr)
		if (result.deg != 1):
			raise cls.PolynominalError(f"affecting polynomial with deg {result.deg} to deg one polynomial")
		else:
			return cls(result.coefs)
		#print(Error)
