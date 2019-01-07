from django.views.decorators.csrf import csrf_exempt
from sympy import *
import sympy as sy
from sympy import simplify
from sympy.abc import x, y, z
import random

def generate_simple_qe():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    out = ""
    if random.randint(0, 2) == 0:
        out += "-"
    out += str(a) + "x^2"

    out += "-" if random.randint(0, 2) == 1 else "+"
    out += str(b) + "x"

    out += "-" if random.randint(0, 2) == 0 else "+"
    out += str(c) + "=0"
    return out


def get_random_result(prb=25):
    number = random.randint(1, 100)
    return number == prb


def generate_six_one():
    x, y, z = symbols('x y z')
    k = random.randint(1, 10)
    chapter6_1 = [((k * x) * cos(x)), ((k * x) * cos(pi * x)), (k * x) * (1 / sin(x)), ((k * x) ** 2) * (1 / tan(x)),
                  (k * x) * ((ln(x)) ** 3), 1 / tan(x), ((k * x) ** 3) * ln(k * x), (x + k) * sy.exp(k * x),
                  (x + k) * sy.exp(k * x)]
    chapter6_2 = [(1 / sy.sqrt(k - (k * (x ** 2)))), (x ** 3) / sy.sqrt(9 + x ** 2), sy.sqrt(9 + x ** 2) / (x ** 4),
                  1 / sy.sqrt(9 + x ** 2), 1 / (x * sy.sqrt(9 - x ** 2)), (k * (x ** 2)) / sy.sqrt(k - (k * (x ** 2))),
                  1 / ((k * x ** 2) * sy.sqrt(9 - x ** 2)), (k * x + k) / sy.sqrt(9 - x ** 2),
                  k * (x ** 2) / sy.sqrt(k - (x ** 2)), k * (x ** 2) / sy.sqrt(k - (x ** 2))]
    expression = random.choice(chapter6_1)
    # pprint(Integral(expression, x), use_unicode=True)
    return str(expression)

def solve_six_one(expr, answer):
    if simplify(integrate(expr, x) - eval(answer)) == 0:
        return True
    else:
        return False

def answer_six_one(expr):
    return simplify(integrate(expr, x))
