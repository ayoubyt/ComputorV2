from inspect import signature
from typing import Callable, Any, List
import re

from .type import Type

class Function(Type):
    def __init__(self, fn: Callable[..., Any], name: str = "anonymouse") -> None:
        self.name = name
        self.vars = list(signature(fn).parameters)
        self.expr = "[built-in]"
        self.fn = fn
        self.varnum = len(signature(fn).parameters)

    def __call__(self, *args, **kwds):
        return self.fn(*args, **kwds)

    def __str__(self) -> str:
        return f"{self.name}({','.join(self.vars)})={self.expr}"


class ListFunction(Function):
    pattern = r"[a-zA-Z]+\(.+\)"
    def __init__(self, expr: str, vars: List[str],  name: str = "anonymouse") -> None:
        self.name = name
        self.expr = expr
        self.vars = vars
        self.varnum = len(vars)
        from ..expression import infix_to_rpnlist
        rpn_list = infix_to_rpnlist(expr)
        for i in range(len(rpn_list)):
            if (rpn_list[i] in vars):
                rpn_list[i] = str(vars.index(rpn_list[i]))
        self.rpn_list = rpn_list

    def __call__(self, *args, **kwds):
        res = self.rpn_list.copy()
        for i in range(len(self.rpn_list)):
            if isinstance(res[i], str) and res[i].isdigit():
                res[i] = args[int(res[i])]
        from ..expression import eval_rpn
        return eval_rpn(res)

    def subvars(self):
        # a function to replace variables with there values
        def f(m: re.Match):
            from ..ft_global import user_vars
            word = m.group().lower()
            if word in user_vars and not isinstance(user_vars[word], Function):
                return(str(user_vars[word]))
            else:
                return(m.group())
        result = re.sub(r"[a-zA-Z]+", f, self.expr)
        return result.strip()

    def __str__(self) -> str:
        result = self.subvars()
        return f"{self.name}({','.join(self.vars)}) = {result}"
