from .polynomial import Polynomial
from .. import func

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
		b, a = self.coefs
		print(self, "= 0")
		print("a first degree equation with one solution :")
		print("x = %f" % (-b / a))



	@classmethod
	def fromexpr(cls, expr):
		result = Polynomial.fromexpr(expr)
		if (result.deg != 1):
			raise cls.PolynominalError(f"affecting polynomial with deg {result.deg} to deg one polynomial")
		else:
			return cls(result.coefs)
		#print(Error)
