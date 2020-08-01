from math import sqrt
import re
from abc import ABC
from .ft_global import ComputerV2Exception
from .ft_math import ft_sqrt

class Var(ABC):
    pass

##################################################

class Complex(Var):

    _real_patern = r"\d+(?:\.\d+)?"
    pattern = (r"(-?{})([+-]{})i".format(_real_patern, _real_patern))

    def __init__(self, *args, **kwargs) -> None:
        if (len(args) == 1 and type (args[0]) is str):
            expr : str = re.sub(r"\s+", "", args[0])
            match = re.fullmatch(Complex.pattern, expr)
            if match:
                self.re, self.im = list(map(float, match.groups()))
            else:
                raise ComputerV2Exception("string must match patern 'x(+/-)yi' where x and y are real numbers")
        elif (len(args) == 2):
            self.re, self.im = float(args[0]), float(args[1])
        else:
            raise ComputerV2Exception("invalid input")

    def __add__(self, other):
        if (isinstance(other, Complex)):
            return Complex(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        if (isinstance(other, Complex)):
            return Complex(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        if (isinstance(other, Complex)):
            re = self.re * other.re - self.im * other.im
            im = self.re * other.im + self.im * other.re
            return Complex(re, im)

    def __truediv__(self, other):
            if (isinstance(other, Complex)):
                return self * other.inv

    @property
    def inv(self):
        mag2 =  (self.re ** 2 + self.im ** 2)
        conj = self.conj
        return Complex(conj.re / mag2, conj.im / mag2)

    @property
    def mag(self):
        return ft_sqrt(self.re * self.re + self.im * self.im)

    @property
    def conj(self):
        return Complex(self.re, -self.im)

    def __str__(self) -> str:
        return f"{self.re}{self.im:+}i"


class Real(Complex):
    pattern = (Complex._real_patern)
    def __init__(self, value) -> None:
        super().__init__(value, 0)

    def __str__(self) -> str:
        return "%d" % (self.re)

class Im(Complex):
    pattern = (f"{Complex._real_patern}i")
    def __init__(self, value) -> None:
        if type(value) is str:
            expr : str = re.sub(r"\s+", "", value)
            match = re.fullmatch(f"({Complex._real_patern})i?", expr)
            if match:
                self.re, self.im = 0, float(match.groups()[0])
            else:
                raise ComputerV2Exception("string must match patern 'x(+/-)yi' where x and y are real numbers")
        else:
            super().__init__(0, value)

    def __str__(self) -> str:
        return "%di" % (self.im)



######################################################

class Matrix(Var):
    pattern = (r"\[\[.*?\]\]")

class Vector(Matrix):
    pattern = r"\[.*?\]"
