from .type import Type

class Matrix(Type):
    pattern = (r"\[\[.*?\]\]")

class Vector(Matrix):
    pattern = r"\[.*?\]"

