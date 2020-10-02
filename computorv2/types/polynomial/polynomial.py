import re
from collections import deque
from ..function import ListFunction


class Polynomial:
    """
        Polynomial class respresents aplonominal hh
        you initiaise it by in inputing an array of the coefficients of tha polynomanal ordered from left to right
        ex: 1 + 5x + 2x^2 --> plonominal([1, 5, 2])
    """

    def __init__(self, coefficients):
        self.coefs = self.__trim_coefs(coefficients)
        self.deg = len(self.coefs) - 1

    def __trim_coefs(self, coefs):
        """
        __trim_coef is privat function designed to remove all
        the nonsense zeros that the user inputs at the end of the array of coefficients
        """
        while (len(coefs) > 1 and coefs[-1] == 0):
            coefs.pop()
        return (coefs)

    def __str__(self):
        res = ""
        if (len(self.coefs) < 1):
            return ("0")
        for i, co in enumerate(self.coefs):
            if (co != 0):
                co = int(co) if isinstance(co, int) or (
                    co).is_integer() else float("%.2f" % co)
                if (i > 0):
                    res += " + " if co > 0 else " - "
                    if (abs(co) != 1):
                        res += str(abs(co))
                    res += "x^%d" % i if i > 1 else "x"
                else:
                    res += str(co)
        return res

    def __add__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("+", other).coefs
        if (len(p2) > len(p1)):
            p1, p2 = p2, p1
        for i, co in enumerate(p2):
            p1[i] += co
        return (Polynomial(p1))

    def __sub__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("-", other).coefs
        if (len(p2) > len(p1)):
            p1, p2 = list(map(lambda x: -x, p2)), list(map(lambda x: -x, p1))
        for i, co in enumerate(p2):
            p1[i] -= co
        return (Polynomial(p1))

    def __mul__(self, other):
        p1 = self.coefs
        p2 = self._set_op_param("*", other).coefs
        l = len(p1) + len(p2) - 2
        result = [0] * (l + 1)
        for i in range(l + 1):
            for j in range(i + 1):
                result[i] += (p1[j] if j < len(p1) else 0) * \
                    (p2[i - j] if i - j < len(p2) else 0)
        return Polynomial(self.__trim_coefs(result))

    def __truediv__(self, other):
        p1 = self.coefs
        n = int(self._set_op_param("/", other).coefs[0])

        for i in range(len(p1)):
            p1[i] /= n
        return Polynomial(p1)

    def __pow__(self, other):
        p1 = self
        n = int(self._set_op_param("**", other).coefs[0])
        result = p1
        if (n == 0):
            return Polynomial([1])
        for _ in range(n - 1):
            result = result * p1
        return result

    def _set_op_param(self, op, other):
        if (not isinstance(other, Polynomial)):
            if (isinstance(other, int) or isinstance(other, float)):
                return Polynomial([other])
            else:
                raise self.PolynominalError(
                    f"{op} is not suported for Polyomial an {type(other)}")
        else:
            if ((op == "/" or op == "**") and other.deg > 0):
                if op == "/":
                    raise self.PolynominalError(
                        "can't divide by a Polynomial with deg more than 0 (real number)")
                if op == "**":
                    raise self.PolynominalError(
                        "can't raise a polynomina with deg more than 0 (real number) to another Polynomial")
            return other

    @classmethod
    def parse_to_plynomainals(cls, str):
        pass

    @classmethod
    def fromexpr(cls, expr):
        # this function transform an arrays of elements to a deque

        # remove whitespacecs
        # print(expr)
        expr = re.sub(r"\s", "", expr)
        expr = re.sub(
            r"(^|[+*/)(])-", r"\1-1*", expr)
        # putting '*' in its place
        expr = re.sub(
            r"(?:(-?\d+(?:\.\d+)?|[a-zA-Z])(?=[a-zA-Z\(]))", r"\1*", expr)
        expr = re.sub(
            r"(?:([\)])(?=(?:-?\d+(?:\.\d+)?|[a-zA-Z]|\()))", r"\1*", expr)
    # print(expr)
        elements = re.findall(
            r"(?<![\w)])-?(?:\d+(?:\.\d+)?|[a-zA-Z])|[\*/+()^]|(?<=[\w)])-", expr)
    # print(elements)
        postfix = cls._to_postfix(elements)
        print(f"{postfix=}")
    #print(" ".join(postfix))
        result = cls._eval_postfix(postfix)
        # print(result)
        return result

    @classmethod
    def _to_postfix(cls, arr):
        """
                        takes an array of elements of an expression
                        an returns a queue of elemts represents a postfix
                        notation of the first expresstion
        """
        ops = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        opstack = deque()
        output = []
        for c in arr:
            if c in ops:
                while (len(opstack) > 0) and (opstack[-1] in ops) and (ops[c] <= ops[opstack[-1]]):
                    if (c != "^"):
                        output.append(opstack.pop())
                opstack.append(c)
            elif (c in "()"):
                if (c == "("):
                    opstack.append(c)
                else:
                    while (len(opstack) > 0):
                        tmp = opstack.pop()
                        if (tmp == "("):
                            break
                        else:
                            output.append(tmp)
            else:
                output.append(c)
            #print("output : ", output)
            #print("opsstack: ", opstack, end="\n\n")
        while(len(opstack) > 0):
            output.append(opstack.pop())
        return(output)

    @classmethod
    def (cls, postfix):
        """
                takes an array of string elements of a mathematical expresion
                in postfix notation and evaluats it returning a single polynominal
        """
        ops = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        polystack = deque()
        for elem in postfix:
            if (elem in ops):
                if (len(polystack) > 1):
                    a = polystack.pop()
                    b = polystack.pop()
                    if (elem == "+"):
                        polystack.append(b + a)
                    elif (elem == "-"):
                        polystack.append(b - a)
                    elif (elem == "*"):
                        polystack.append(b * a)
                    elif (elem == "/"):
                        polystack.append(b / a)
                    elif (elem == "^"):
                        polystack.append(b ** a)
                else:
                    raise cls.PolynominalError(
                        "number of operators is mor than operands.")
            else:
                if (re.search(r"[a-zA-Z]", elem)):
                    polystack.append(
                        (cls([0, -1]) if re.search(r"^-", elem) else cls([0, 1])))
                else:
                    polystack.append(cls([float(elem)]))
        return polystack.pop()

    class PolynominalError(Exception):
        msg = ""

        def __init__(self, msg):
            self.msg = msg
            Exception.__init__(self, msg)

        def __str__(self):
            return (self.msg)
