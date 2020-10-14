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
    varName = re.sub(r"\s+", "", varName)
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
        res = expr
        user_vars[m.group(1)] = ListFunction(expr, variables, m.group(1))
    else:
        raise ComputerV2Exception(
            f"invalid varibale name '{varName}', should only contain letters")
    return res


def eval_expression(text: str):
    expr = text.split("=")[0]
    return calc(expr)


def eval_input(text: str):
    # remove whitespaces from both ends
    text = text.strip()
    res: str = ""
    if (len(text) == 0):
        return text
    if (text[0] == ":"):
        eval_command(text)
        return ""
    if "=" in text:
        if text.count("=") > 1:
            raise NameError("just one '=' symbole must be in the expression")
        if (text[-1] == "?"):
            return eval_expression(text)
        else:
            return eval_asignment(text)
    else:
        return calc(text)
