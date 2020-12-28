# import os
# import sys
# sys.path.insert(0, os.path.join(sys.path[0], '..'))
# from computorv2.main import eval_input

import pexpect as pe
import re
import unittest


# defigns

propmpt = ">"

ps = pe.spawn("python bin/computorv2.py")
ps.expect(propmpt)
ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def type_line(text):
    ps.sendline(text)
    ps.expect("\r\n")
    ps.expect(propmpt)
    res = ansi_escape.sub("", ps.before.decode()).strip()
    return res


class TestNumCalc(unittest.TestCase):

    def test_number_simple_calculations(self):
        test_cases = [
            ("-2 =?", f"{-2}"),
            ("2 * -1 + 1 =?", f"{2 * -1 + 1}"),
            ("1 + 1 =?", "2"),
            ("1 / 3 =?", f"{1 / 3:.6}"),
            ("0.2 *0.2 * 10 / 5", f"{0.2 *0.2 * 10 / 5:.6}"),

        ]

        for test in test_cases:
            result = type_line(test[0])
            print("testing if : ", "'", test[0], "'", " == ", test[1])
            self.assertEqual(result, test[1])

    def test_number_weird_calculations(self):
        test_cases = [
            ("2 * 0-(4 * 2)", f"{2 * 0-(4 * 2)}"),
            ("1 + 2 + 3 * 5 + 4 * (2 + 1 * 8 -(2*3*6-5*(4+1+2+9*6-5/4/2)))/6=?",
                f"{1 + 2 + 3 * 5 + 4 * (2 + 1 * 8 -(2*3*6-5*(4+1+2+9*6-5/4/2)))/6:.6}")
        ]

        for test in test_cases:
            result = type_line(test[0])
            print("testing if : ", "'", test[0], "'", " == ", test[1])
            self.assertEqual(result, test[1])

class TestAssign(unittest.TestCase):

    def test_number_simple_asignment(self):
        test_cases = [
           ("a = 1", "1"),
           ("a + 1 =?", "2")
        ]

        for test in test_cases:
            result = type_line(test[0])
            print("testing if : ", "'", test[0], "'", " == ", test[1])
            self.assertEqual(result, test[1])


if __name__ == "__main__":
    unittest.main()
