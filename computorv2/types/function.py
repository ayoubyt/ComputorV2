from .type import Type
from inspect import signature
from typing import Callable, Any, List


class Function(Type):
    def __init__(self, fn: Callable[..., Any], name: str = "anonymouse") -> None:
        self.name = name
        self.fn = fn
        self.from_function = True
        self.varnum = len(signature(fn).parameters)

    def __call__(self, *args, **kwds):
        return self.fn(*args, **kwds)


class ListFunction(Function):
    def __init__(self, expr: str, vars: List[str],  name: str = "anonymouse") -> None:
        self.name = name
        self.varnum = len(vars)
        from ..expression import infix_to_rpnlist
        rpn_list = infix_to_rpnlist(expr)
        for i in range(len(rpn_list)):
            if (rpn_list[i] in vars):
                rpn_list[i] = str(vars.index(rpn_list[i]))
        self.rpn_list = rpn_list

    def __call__(self, *args, **kwds):
        for i in range(len(self.rpn_list)):
            if isinstance(self.rpn_list[i], str) and self.rpn_list[i].isdigit():
                self.rpn_list[i] = args[int(self.rpn_list[i])]
        from ..expression import eval_rpn
        return eval_rpn(self.rpn_list)
