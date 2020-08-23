from xeger import Xeger
from random import *
import sympy


operatorNoPat = "[+-]\\ {0,1}"
operatorPat = "\\ {0,1}[+-]\\ {0,1}"
multPat = "\\ {0,1}\\*\\ {0,1}"
consPat = "[+-]?[1-9][0-9]{0,1}"
monoPat = "x( {0,1}\*\* {0,1}[+]?[1-4][0-9]?)?"
leftPat = "\\ {0,1}\\(\\ {0,1}"
rightPat = "\\ {0,1}\\)\\ {0,1}"
indexPat = "(\*\* {0,1}[+]?[1-4][0-9]?)?"
MAXmonoPat="x\\*\\*9999\\*x\\*\\*2"
ZEROconsPat = "[+-]?0"
ZEROmonoPat = "x( {0,1}\\*\\* {0,1}[+-]?0)?"
pat = Xeger(limit=20)
nest = 0


def derivative_judge(ans, fx, wf_raise=True):
    my_answer = ans.strip()
    if my_answer == "":
        return False
    if my_answer == "WRONG FORMAT!":
        if wf_raise:
            raise ValueError("wrong format")
        else:
            return False
    n = uniform(-10, 10)
    x = sympy.Symbol('x')
    ture_value = sympy.diff(fx, 'x').evalf(subs={x: n})
    my_value = sympy.sympify(my_answer).evalf(subs={x: n})

    return my_value == ture_value


def hw1_generator(length):
    ans = ""
    for i in range(length):
        ans += str(randint(-9, 9)) + "*x**" + \
               str(randint(-9, 9)) + "+"
    return ans[:-1]


def hw2_generator(times, max_length=100):
    s = _hw2_generate_poly(times)
    while len(s) > max_length:
        s = _hw2_generate_poly(times)
    return s


def hw3_generator(length):
    s = _hw3_generate_poly()
    while len(s) > length:
        s = _hw3_generate_poly()
    return s


def _hw3_generate_poly():
    poly = ""
    operator = randint(0, 1)
    if operator:
        poly += pat.xeger(operatorPat)
    poly += _hw3_generate_term()
    if nest:
        times = randint(0, 1)
    else:
        times = randint(0, 2)
    for i in range(0, times):
        poly += pat.xeger(operatorPat) + _hw3_generate_term()
    return poly


def _hw3_generate_term():
    term = ""
    operator = randint(0, 1)
    if operator:
        term += pat.xeger(operatorNoPat)
    term += _hw3_generate_factor()
    if nest:
        times = randint(0, 2)
    else:
        times = randint(0, 4)
    for i in range(0, times):
        term += pat.xeger(multPat) + _hw3_generate_factor()
    return term


def _hw3_generate_factor():
    global nest
    if nest < 3:
        factor_type = randint(1, 5)
    else:
        factor_type = randint(1, 2)
    factor = ""
    if factor_type == 1:
        factor = pat.xeger(consPat)
    elif factor_type == 2:
        factor = pat.xeger(monoPat)
    elif factor_type == 3:
        nest += 1
        factor = "sin" + pat.xeger(leftPat) + _hw3_generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 4:
        nest += 1
        factor = "cos" + pat.xeger(leftPat) + _hw3_generate_factor() + pat.xeger(rightPat) + pat.xeger(indexPat)
        nest -= 1
    elif factor_type == 5:
        nest += 1
        factor = "(" + _hw3_generate_poly() + ")"
        nest -= 1
    return factor


def _hw2_generate_poly(times):
    poly = ""
    operator = randint(0, 1)
    if operator:
        poly += pat.xeger(operatorPat)
    poly += _hw2_generate_term()
    for i in range(0, times):
        poly += pat.xeger(operatorPat) + _hw2_generate_term()
    return poly


def _hw2_generate_term():
    term = ""
    operator = randint(0, 1)
    if operator:
        term += pat.xeger(operatorNoPat)
    term += _hw2_generate_factor()
    if nest:
        times = randint(0, 2)
    else:
        times = randint(0, 5)  ###
    for i in range(0, times):
        term += pat.xeger(multPat) + _hw2_generate_factor()
    return term


def _hw2_generate_factor():
    global nest
    if nest < 3:
        factor_type = randint(1, 5)
    else:
        factor_type = randint(1, 2)
    factor = ""
    if factor_type == 1:
        factor = pat.xeger(choice([consPat,consPat,consPat,consPat,consPat,consPat,consPat,consPat,consPat,ZEROconsPat]))
    elif factor_type == 2:
        factor = pat.xeger(choice([monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,monoPat,MAXmonoPat,ZEROmonoPat]))
    elif factor_type == 3:
        nest += 1
        factor = "sin(x)**"+str(randint(-5,5))
        nest -= 1
    elif factor_type == 4:
        nest += 1
        factor = "cos(x)**"+str(randint(-5,5))
        nest -= 1
    elif factor_type == 5:
        nest += 1
        factor = choice(["sin(x)","cos(x)"])
        nest -= 1
    return factor


if __name__ == "__main__":
    print(hw1_generator(5))