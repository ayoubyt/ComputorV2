from enum import Enum, auto
from typing import Dict

vars = {}


class EvalDir(Enum):
    """
    an enum to hold avaluation execution direction of
    an operator
    """
    LTOR = auto()
    RTOL = auto()
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
    "^": {
        "precedence": 4,
        "eval_dir": EvalDir.RTOL
    },
    "*": {
        "precedence": 3,
        "eval_dir": EvalDir.LTOR
    },
    "/": {
        "precedence": 3,
        "eval_dir": EvalDir.LTOR
    },
    "+": {
        "precedence": 2,
        "eval_dir": EvalDir.LTOR
    },
    "-": {
        "precedence": 2,
        "eval_dir": EvalDir.LTOR
    }
}


class ComputerV2Exception(Exception):
    def __init__(self, message) -> None:
        super().__init__("\033[91merror : \033[0m" + message)
