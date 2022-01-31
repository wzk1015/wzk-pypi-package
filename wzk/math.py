from collections import defaultdict
from tabulate import tabulate
from time import sleep

"""
单纯形算法
输入：
    max z = 2x1+3x2
    s.t. x1 + 2x2 <= 8
         4x1      <= 16
              4x2 <= 12
         x1 >= 0
         x2 >= 0
输出：
    //每一次更新后的单纯形表
    +-----+-----+------+------+--------+-------+------+------+------+
    | 基   |   z |   x1 |   x2 |     s1 |    s2 |   s3 |   s4 |    解 |
    +=====+=====+======+======+========+=======+======+======+======+
    | z   |   1 |    0 |    0 |  0.75  |  0.5  |    0 |    0 | 21   |
    +-----+-----+------+------+--------+-------+------+------+------+
    | x1  |   0 |    1 |    0 |  0.25  | -0.5  |    0 |    0 |  3   |
    +-----+-----+------+------+--------+-------+------+------+------+
    | x2  |   0 |    0 |    1 | -0.125 |  0.75 |    0 |    0 |  1.5 |
    +-----+-----+------+------+--------+-------+------+------+------+
    | s3  |   0 |    0 |    0 |  0.375 | -1.25 |    1 |    0 |  2.5 |
    +-----+-----+------+------+--------+-------+------+------+------+
    | s4  |   0 |    0 |    0 |  0.125 | -0.75 |    0 |    1 |  0.5 |
    +-----+-----+------+------+--------+-------+------+------+------+
    z = 21.0 achieved when x1 = 3.0, x2 = 1.5, 
"""


class SimplexLexer:
    def __init__(self, s: str):
        self.source = s
        self.ch = ""
        self.pos = 0
        self.reserves = {
            "max" : "MAXTK",
            "min" : "MINTK",
            "s.t.": "STTK"
        }

    def read_char(self):
        self.ch = self.source[self.pos]
        self.pos += 1

    def retract(self):
        self.pos -= 1

    def end(self):
        return self.pos >= len(self.source)

    def get_token(self):
        token = ""
        symbol = ""
        self.read_char()
        while self.ch in [" ", "\n", "\r", "\t", "*"] and not self.end():
            self.read_char()
        if self.end():
            raise ValueError("unexpected end of tokens")
        if self.ch.isalpha():
            while self.ch.isalnum() or self.ch in ["_", "."]:
                token += self.ch
                self.read_char()
            self.retract()
            if token in self.reserves.keys():
                symbol = self.reserves[token]
            else:
                symbol = "IDENTF"
        elif self.ch.isnumeric() or self.ch == "-":
            while self.ch.isnumeric() or self.ch in [".", "-"]:
                token += self.ch
                self.read_char()
            self.retract()
            symbol = "NUMCON"
        elif self.ch == "<":
            self.read_char()
            if self.ch == "=":
                token, symbol = "<=", "LEQ"
            else:
                token, symbol = "<", "LSS"
                self.retract()
        elif self.ch == ">":
            self.read_char()
            if self.ch == "=":
                token, symbol = ">=", "GEQ"
            else:
                token, symbol = ">", "GRE"
                self.retract()
        elif self.ch == "=":
            token, symbol = "=", "EQL"
        elif self.ch == "+":
            token, symbol = "+", "PLUS"
        elif self.ch == "-":
            token, symbol = "-", "MINUS"
        else:
            raise ValueError("unknown character: " + self.ch)
        return token, symbol


class SimplexSolver:
    def __init__(self, s):
        self.lexer = SimplexLexer(s)
        self.sym = ""
        self.str = ""
        self.variables = []
        self.equations = []
        self.old = None
        self.objective = None
        self.obj_equation = defaultdict(float)
        self.table = []

    def next_sym(self):
        self.old = (self.str, self.sym)
        self.str, self.sym = self.lexer.get_token()

    def error(self, expected):
        raise ValueError("expected " + expected + ", got " + self.str + ", type: " + self.sym)

    def solve(self):
        self.analyze()
        self.init_table()
        self.show_table()
        while not self.end():
            self.update()
            self.show_table()
            sleep(0.5)

        print(self.objective + " =", self.table[0][-1], "achieved when", end=" ")
        first_row = [l[0] for l in self.table]
        for v in self.variables:
            if v in first_row:
                print(v + " =", round(self.table[first_row.index(v)][-1], 2), end=", ")
            else:
                print(v + " = 0", end=", ")

    def update(self):
        col = self.table[0][2:-1].index(min(self.table[0][2:-1])) + 2
        enter = self.variables[col - 2]
        min_v, min_line = 1e10, None
        for i in range(1, self.num_lines):
            v = self.table[i][-1] / self.table[i][col] if self.table[i][col] != 0 else 1e10
            if min_v > v >= 0:
                min_v = v
                min_line = i
        if min_line is None:
            raise ValueError("out-of-bound solution")
        self.table[min_line][0] = enter
        pivot = self.table[min_line][col]
        self.table[min_line][1:] = [v / pivot for v in self.table[min_line][1:]]
        for i in range(self.num_lines):
            if i != min_line:
                pivot = self.table[i][col]
                self.table[i][1:] = [self.table[i][idx] - pivot * self.table[min_line][idx]
                                     for idx in range(1, self.num_rows)]

    def init_table(self):
        self.num_base = len(self.equations)
        self.num_lines = self.num_base + 1
        self.num_rows = len(self.variables) + self.num_base + 3
        self.bases = ["s" + str(i + 1) for i in range(self.num_base)]
        self.variables.sort()
        first_line = [self.objective, 1]
        for var in self.variables:
            first_line.append(-1 * self.obj_equation[var])
        for i in range(self.num_base):
            first_line.append(0)
        first_line.append(0)
        assert len(first_line) == self.num_rows, str(first_line) + " " + str(self.num_rows)
        self.table.append(first_line)

        for i in range(self.num_base):
            cur_line = ["s" + str(i + 1), 0]
            for var in self.variables:
                cur_line.append(self.equations[i][var])
            for j in range(self.num_base):
                cur_line.append(1 if j == i else 0)
            cur_line.append(self.equations[i]["const"])
            assert len(cur_line) == self.num_rows
            self.table.append(cur_line)

    def show_table(self):
        head = ["基", self.objective, *self.variables, *self.bases, "解"]
        assert len(head) == self.num_rows
        print(tabulate(self.table, headers=head, tablefmt="grid"))

    def end(self):
        return min(self.table[0][2:-1]) >= 0

    def analyze(self):
        self.next_sym()
        if self.sym not in ["MAXTK", "MINTK"]:
            self.error("max or min")
        self.next_sym()
        if self.sym != "IDENTF":
            self.error("identifier")
        self.objective = self.str
        self.next_sym()
        if self.sym != "EQL":
            self.error("'='")
        self.next_sym()
        self.obj_equation.update(self.linear())
        if self.sym != "STTK":
            self.error("'s.t.'")
        while not self.lexer.end():
            self.next_sym()
            equ = self.linear()
            if self.sym not in ["LEQ", "GEQ"]:
                self.error("'<='")
            if self.sym == "GEQ":
                return  #ignore >= 0
            self.next_sym()
            if self.sym != "NUMCON":
                self.error("positive number")
            assert "const" not in equ.keys()
            equ["const"] = float(self.str)
            self.equations.append(equ)

    def linear(self):
        ans, v = defaultdict(float), 1
        if self.sym == "NUMCON":
            if self.str == "-":
                self.str = "-1"
            v = float(self.str)
            self.next_sym()
        self.identifier()
        ans[self.str] = v
        self.next_sym()
        while self.sym in ["PLUS", "MINUS", "NUMCON"]:
            if self.sym != "NUMCON":
                self.next_sym()
            v = 1
            if self.str == "-":
                self.str = "-1"
            if self.sym == "NUMCON":
                v = float(self.str)
                self.next_sym()
            self.identifier()
            ans[self.str] = v
            self.next_sym()
        return ans

    def identifier(self):
        if self.sym != "IDENTF":
            self.error("identifier")
        elif self.str not in self.variables:
            assert self.str[0] != "s"
            self.variables.append(self.str)


def is_prime(a: int):
    for i in range(2, int(a ** 0.5 + 1)):
        if a % i == 0:
            return False
    return True


def primes(num, upper_bound=0.0):
    ans = []
    i = 2
    while True:
        if is_prime(i):
            ans.append(i)
            print(i, end=" ")
        if len(ans) == num != 0:
            break
        if i > upper_bound != 0:
            break
        i += 1
    return ans


def factorize(n):
    ans = []
    i = 2
    while True:
        if not is_prime(i):
            i += 1
            continue
        #print(i, end=" ")
        while n % i == 0:
            ans.append(i)
            print("div", i)
            n = n // i
            print("remain", n)
        i += 1
        if n == 1:
            break
    return ans


if __name__ == '__main__':
    # s = "max z = 2x1 + x2  \
    #     s.t. x1-x2 <= 10 \
    #     x1 >= 0 \
    #     x2 >= 0  \
    #     2x2 <= 40"
    # s = "min z = 7x1 + 9x2 + 10x3  \
    #     s.t.  \
    #     x1-2x3 <= 8 \
    #     -2x2+8x3 <= -1 "
    # solver = SimplexSolver(s)
    # solver.solve()
    #print(is_prime(127789007))
    print(factorize(110102199910152711))


