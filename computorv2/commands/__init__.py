from computorv2.exceptions import ComputerV2Exception
import re
from .ft_print import cmd_print

commands = {
    "print"  : cmd_print
}


def eval_command(text :str):
    cmd_match = re.match(r":(.+?)\b", text)
    if not cmd_match:
        raise ComputerV2Exception("invalid input")
    params = re.sub(r":[a-zA-Z]+", "", text)
    try:
        commands[cmd_match.group(1).lower()](params)
    except KeyError:
        raise ComputerV2Exception(f"no comand named '{cmd_match.group(1)}'")

