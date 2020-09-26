from enum import Enum, auto
from .types import Function
from . import ft_math

builtin_vars = {
    "sqrt": Function(ft_math.ft_sqrt, "sqrt"),
    "max": Function(ft_math.ft_max, "max"),
    "min": Function(ft_math.ft_min, "min"),
}

user_vars = {
}


class EvalDir(Enum):
    """
    an enum to hold avaluation execution direction of
    an operator
    """
    # left to right
    LTOR = auto()
    # right to left
    RTOL = auto()
    # not an operator
    NONE = auto()


operators = {
    "(": {
        "precedence": -1,
        "eval_dir": EvalDir.NONE
    },
    ")": {
        "precedence": -1,
        "eval_dir": EvalDir.NONE
    },
    ",": {
        "precedence": -1,
        "eval_dir": EvalDir.NONE
    },
    "^": {
        "precedence": 4,
        "eval_dir": EvalDir.RTOL,
        "func": lambda a, b: a ** b
    },
    ".": {
        "precedence": 2,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a * b
    },
    "*": {
        "precedence": 3,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a * b
    },
    "/": {
        "precedence": 3,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a / b
    },
    "%": {
        "precedence": 3,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a % b
    },
    "+": {
        "precedence": 1,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a + b
    },
    "-": {
        "precedence": 1,
        "eval_dir": EvalDir.LTOR,
        "func": lambda a, b: a - b
    }
}
