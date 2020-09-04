from computorv2.exceptions import ComputerV2Exception
import re
from ..expression import calc
from ..ft_global import user_vars, builtin_vars

# sv stands for special variables
sv_handlers = {
    "vars": lambda: print({key: str(val) for key, val in user_vars.items()}),
    "builtin_vars": lambda: print([str(v) for v in builtin_vars.values()])
}


def cmd_print(params: str):
    tokens = map(str.strip, params.split(","))
    for t in tokens:
        if (t[0] == "$"):
            try:
                sv_handlers[t[1:].lower()]()
            except KeyError:
                raise ChildProcessError(f"special variable '{t}' not found")
        elif m := re.fullmatch(r"[\"'](.+)[\"']", t):
            print(m.group(1), end=" ")
        else:
            print(calc(t), end=" ")
    print()
