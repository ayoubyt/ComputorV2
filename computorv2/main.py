import re
from re import fullmatch
from prompt_toolkit import PromptSession
from .expression import calc
from .exceptions import ComputerV2Exception
from .ft_global import user_vars
from .types.function import ListFunction
from .commands import eval_command

prompt_session = PromptSession()


def eval_asignment(text: str):
    varName, expr = text.split("=")
    if varName.lower() == "i":
        raise ComputerV2Exception(f"can't use '{varName}' as variable name")
    elif (re.fullmatch(r"[a-zA-Z]+", varName)):
        res = calc(expr)
        user_vars[varName] = res
    elif (m := re.fullmatch(r"([a-zA-Z]+)\((.+)\)", varName)):
        variables = m.group(2).split(",")
        for v in variables:
            if not re.fullmatch(r"[a-zA-Z]+", v):
                raise ComputerV2Exception(
                    f"invalid varibale name '{v}' in function, should only contain letters")
        res = " ".join(list(expr))
        user_vars[m.group(1)] = ListFunction(expr, variables, m.group(1))
    else:
        raise ComputerV2Exception(
            f"invalid varibale name '{varName}', should only contain letters")
    return res


def eval_expression(text: str):
    expr = text.split("=")[0]
    return calc(expr)


def eval_input(text: str):
    # remove whitespaces
    text = text.strip()
    res: str = ""
    if (text[0] == ":"):
        eval_command(text)
    elif "=" in text:
        text = re.sub(r"\s+", "", text)
        if text.count("=") > 1:
            raise NameError("just one '=' symbole must be in the expression")
        if (text[-1] == "?"):
            res = eval_expression(text)
        else:
            res = eval_asignment(text)
    else:
        if (text):
            res = calc(text)
    return res
