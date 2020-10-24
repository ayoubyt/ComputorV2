import pexpect as pe
import re

test_cases = ["555+555i =?", "[[1, 1]]"]

propmpt = ">"

ps = pe.spawn("python bin/computorv2.py")
ps.expect(propmpt)
ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')



for t in test_cases:
    ps.sendline(t)
    ps.expect("\r\n")
    ps.expect(propmpt)
    user_res = ansi_escape.sub("", ps.before.decode()).strip()
    print(ansi_escape.sub("", ps.before.decode()).strip())
