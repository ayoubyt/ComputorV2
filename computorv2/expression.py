import re
from collections import deque
from .var import Var, Real, Im, Matrix, Vector
from .ft_global import ComputerV2Exception, operators, EvalDir


def infix_to_rpn(text):
    types = [Im, Real, Matrix, Vector]
    types_patterns = [C.pattern for C in types]
    ops_patterns = ["\\" + e for e in operators]

    # this line return a list of tuples of matches
    # every match retuns in an index in the tuple
    tokens = re.findall(
        "|".join("(" + x + ")" for x in types_patterns + ops_patterns),
        text
    )

    # in this line, we turn variable expressions (like '2i')
    # to an instance of a variable classe ('2i -> Im('2i'))
    classed_tokens = []
    for e in tokens:
        for i, ne in enumerate(e):
            if ne:
                if (i < len(types)):
                    classed_tokens.append(types[i](ne))
                else:
                    classed_tokens.append(ne)

    rpn = []
    ops_stack = deque()

    for e in classed_tokens:
        if (isinstance(e, Var)):
            rpn.append(e)
        elif (e in operators):
            if (e == ")"):
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
                    last_op = operators[ops_stack[-1]]
                    if (last_op["precedence"] > operators[e]["precedence"]):
                        rpn.append(ops_stack.pop())
                    elif (last_op["precedence"] == operators[e]["precedence"] and operators[e]["eval_dir"] == EvalDir.LTOR):
                        rpn.append(ops_stack.pop())
                    else:
                        break
                ops_stack.append(e)
    while (len(ops_stack) > 0):
        rpn.append(ops_stack.pop())

    print([str(e) for e in rpn])
    return [str(e) for e in classed_tokens]
