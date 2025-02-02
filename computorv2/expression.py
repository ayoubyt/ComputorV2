import re
from collections import deque

from .types import Complex, Type, Real, Im, Matrix, Function, ListFunction
from .exceptions import ComputerV2Exception
from .ft_global import operators, EvalDir, user_vars, builtin_vars

def negatify(expr: str):
    """
    substitue negative numbers to more sutable format for other parsers.
    for example '2*-1' would be '2*(0-1)' etc.
    """
    ops = "".join(
        ["\\" + e for e in operators if operators[e]["precedence"] > 0])
    return re.sub(f"([{ops}])-({Im.pattern}|{Real.pattern}|{ListFunction.pattern}|[a-zA-Z]+)", r"\1(0-\2)", expr)


def check_brackets(text: str):
    left, right = "([", ")]"
    stack = deque()
    for l in text:
        if l in left:
            stack.append(l)
        if l in right:
            try:
                tmp = stack.pop()
                if right.index(l) != left.index(tmp):
                    raise ComputerV2Exception(
                        f"mixed brackets '{tmp}' and '{l}'")
            except IndexError:
                raise ComputerV2Exception(f"unmached bracket {l}")
    if len(stack) > 0:
        raise ComputerV2Exception(f"unmached bracket {stack[-1]}")


def preprocesse(text: str):
    text = re.sub(r"\s+", "", text)

    # check for unmached brackets
    check_brackets(text)

    text = re.sub(r"\*\*", ".", text)
    # transfrom negative numbers to parsed form ('2 * -1' -> '2 * (0 - 1)')
    text = negatify(text)

    # check if some weird caracters exists

    return text.lower()


def infix_to_rpnlist(text: str):
    vartypes = [Im, Real, Matrix]
    types_patterns = [C.pattern for C in vartypes]
    ops_patterns = ["\\" + e for e in operators]
    vars = {**user_vars, **builtin_vars}

    all_patterns = types_patterns + ops_patterns + [r"[a-zA-Z]+"]

    # preprossessing text
    text = preprocesse(text)

    # return a list of tuples of matches
    # every match retuns in an index in the tuple
    tokens = re.findall(
        "|".join(all_patterns),
        text
    )

    # in this line, we turn variable expressions (like '2i')
    # to an instance of a type classe ('2i -> Im('2i'))
    classed_tokens = []
    types_regex = list(enumerate(re.compile(p) for p in types_patterns))
    for e in tokens:
        for i, r in types_regex:
            if (r.fullmatch(e)):
                classed_tokens.append(vartypes[i](e))
                break
        else:
            classed_tokens.append(e)

    # here we'll substiute varible name with there values
    for i, e in enumerate(classed_tokens):
        if (type(e) is str and e in vars):
            classed_tokens[i] = vars[e]

    # thereverse pilish notation result list
    rpn = []
    # operators que
    ops_stack = deque()

    # print(f"{classed_tokens=}")

    # this is the code when we convert infix to rpn
    for e in classed_tokens:
        if (e in operators):
            if (e == ","):
                while (len(ops_stack) > 0):
                    op = ops_stack[-1]
                    if (op == '(' or op == ","):
                        break
                    rpn.append(ops_stack.pop())
            elif (e == ")"):
                while (len(ops_stack) > 0):
                    op = ops_stack.pop()
                    if (op == '('):
                        break
                    rpn.append(op)
                else:
                    raise ComputerV2Exception("unmached ')'")
            elif e == "(":
                ops_stack.append(e)
            else:
                while(len(ops_stack) > 0):
                    last = ops_stack[-1]
                    if (isinstance(last, Function)):
                        rpn.append(ops_stack.pop())
                    else:
                        last = operators[last]
                        if (last["precedence"] > operators[e]["precedence"]):
                            rpn.append(ops_stack.pop())
                        elif (last["precedence"] == operators[e]["precedence"] and operators[e]["eval_dir"] == EvalDir.LTOR):
                            rpn.append(ops_stack.pop())
                        else:
                            break
                ops_stack.append(e)
        elif (isinstance(e, Function)):
            ops_stack.append(e)
        elif (isinstance(e, Type)):
            rpn.append(e)
        elif (isinstance(e, str)):
            rpn.append(e)
    while (len(ops_stack) > 0):
        rpn.append(ops_stack.pop())

    return rpn


def eval_rpn(rpnlist):
    if (len(rpnlist) == 0):
        raise ComputerV2Exception("empty expression")
    res = deque()
    for e in rpnlist:
        if (e in operators):
            try :
                b = res.pop()
                if (len(res) == 0):
                    if (e == "+" or e == "-"):
                        a = Complex(0, 0)
                    else:
                        raise ComputerV2Exception(
                            f"operator {e} needs 2 oprands got 1")
                else:
                    a = res.pop()
                try:
                    res.append(operators[e]["func"](a, b))
                except ZeroDivisionError:
                    raise ComputerV2Exception("division by zero")
            except IndexError:
                raise ComputerV2Exception(f"not enough oprands for operator '{e}'")
        elif isinstance(e, Function):
            if (len(rpnlist) != 1):
                if (len(res) < e.varnum):
                    raise ComputerV2Exception(
                        f"not enough parameters for function '{e.name}', expected {e.varnum} got {len(res)}")
                params = [res.pop() for _ in range(e.varnum)][::-1]
                res.append(e(*params))
            else:
                return e
        elif (isinstance(e, Type)):
            res.append(e)
        else:
            raise ComputerV2Exception(f"undefined variable '{e}'")
    return res[0]


def calc(expr: str):
    return eval_rpn(infix_to_rpnlist(expr))
