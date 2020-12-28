import re
from re import fullmatch
from .expression import calc
from .exceptions import ComputerV2Exception
from .ft_global import user_vars
from .types.function import ListFunction
from .commands import eval_command
from .types import Polynomial, D1plynominal, D2plynominal


def eval_asignment(text: str):
    varName, expr = text.split("=")
    varName = (re.sub(r"\s+", "", varName)).lower()
    if varName == "i":
        raise ComputerV2Exception(f"can't use '{varName}' as variable name")
    elif (re.fullmatch(r"[a-zA-Z]+", varName)):
        res = calc(expr)
        user_vars[varName] = res
    elif (not varName):
         raise ComputerV2Exception(
                    f"empty variable name")
    elif (m := re.fullmatch(r"([a-zA-Z]+)\((.+)\)", varName)):
        variables = m.group(2).split(",")
        for v in variables:
            if not re.fullmatch(r"[a-zA-Z]+", v):
                raise ComputerV2Exception(
                    f"invalid varibale name '{v}' in function, should only contain letters")
        f = ListFunction(expr, variables, m.group(1))
        user_vars[m.group(1)] = f
        res = f.subvars()
    else:
        raise ComputerV2Exception(
            f"invalid varibale name '{varName}', should only contain letters")
    return res

def eval_equation(text : str):
    left, right = text[:-1].split("=")

    eq_poly = Polynomial.fromexpr(left) - Polynomial.fromexpr(right)

    if (eq_poly.deg == 2):
        return D2plynominal(eq_poly.coefs).solve()
    elif (eq_poly.deg == 1):
        return D1plynominal(eq_poly.coefs).solve()
    elif (eq_poly.deg == 0):
        if (eq_poly.coefs[0] == 0):
            return ("all numbers are solutions to this eqation")
        else:
            return ("absurde expression")
    else:
        return str(eq_poly) +  "= 0\n" +f"eqations of degree {eq_poly.deg} are not suported"



def eval_expression(text: str):
    expr = text.split("=")[0]
    return calc(expr)


def eval_input(text: str) -> str:
    # remove whitespaces from both ends
    text = text.strip()
    if (len(text) == 0):
        return text
    if (text[0] == ":"):
        eval_command(text)
        return ""
    if "=" in text:
        if text.count("=") > 1:
            raise ComputerV2Exception("just one '=' symbole must be in the expression")
        text = re.sub(r"\s+", "", text)
        if (text[-1] == "?"):
            if text[-2] == "=":
                return eval_expression(text)
            return eval_equation(text)
        else:
            return eval_asignment(text)
    else:
        return calc(text)

