from ..exceptions import ComputerV2Exception
from .type import Type
from .complex import Real


class Matrix(Type):
    pattern = (r"\[\[.*?\]\]")

    def __init__(self, body) -> None:
        if (type(body) is str):
            rows = body[1:-1].split(";")
            self.body = []
            from ..expression import calc
            prev = -1
            for r in rows:
                row = []
                nums = r[1:-1].split(",")
                for n in nums:
                    row.append(calc(n))
                if prev != -1 and prev != len(row):
                    raise ComputerV2Exception(
                        "inconsistent number of elements in matrix rows")
                prev = len(row)
                self.body.append(row)
        elif type(body) is list and type(body[0]) is list:
            self.body = body

    @property
    def cols(self):
        return len(self.body[0])

    @property
    def rows(self):
        return len(self.body)

    def __str__(self) -> str:
        res = ""
        for e in self.body:
            res += str([str(n) for n in e]) + "\n"
        return res.strip()

    def __mul__(self, other):
        if self.cols == other.rows:
            res = [[Real(0) for __ in range(other.cols)]
                   for _ in range(self.rows)]
            for i in range(len(res)):
                for j in range(len(res[0])):
                    for k in range(self.cols):
                        res[i][j] += self.body[i][k] * other.body[k][j]
            return Matrix(res)
        else:
            raise ComputerV2Exception(
                "number of columns of first matrix must be equal to number of rows of the second")

    def __add__(self, other):
        if self.cols == other.cols and self.rows == other.rows:
            res = [[Real(0) for __ in range(self.cols)]
                   for _ in range(self.rows)]
            for i in range(len(res)):
                for j in range(len(res[0])):
                    res[i][j] = self.body[i][j] + other.body[i][j]
            return Matrix(res)
        else:
            raise ComputerV2Exception(
                "to add two matricies their dimentions must be equal")

    def __sub__(self, other):
        if self.cols == other.cols and self.rows == other.rows:
            res = [[Real(0) for __ in range(self.cols)]
                   for _ in range(self.rows)]
            for i in range(len(res)):
                for j in range(len(res[0])):
                    res[i][j] = self.body[i][j] - other.body[i][j]
            return Matrix(res)
        else:
            raise ComputerV2Exception(
                "to substract two matricies their dimentions must be equal")


class Vector(Matrix):
    pattern = r"\[.*?\]"
