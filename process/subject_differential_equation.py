import random
from sympy import *

y = Function('y')
x = Symbol('x',  real=True)


def supper():
    return True

def remove_right(e):
    return e.replace("\\right", "").replace("\left", "").replace(" ", "")

def generate_diff_eq():
    n1 = random.randint(1, 15)
    n2 = random.randint(1, 15)
    n3 = random.randint(1, 15)

    chapter = [Eq(n1*y(x).diff(x, x) + n2*y(x).diff(x) + n3*y(x), 0),
                 Eq(n1*y(x).diff(x, x) - n2*y(x).diff(x) - n3*y(x), 0),
                 Eq(n1*y(x).diff(x, x) - n2*y(x).diff(x), 0),
                 Eq(n1*y(x).diff(x, x) + n2*y(x).diff(x), 0),
                 Eq(n1*y(x).diff(x, x) - n2*y(x).diff(x) + n3*y(x), 0),
                 Eq(n1*y(x).diff(x, x) + n2*y(x).diff(x) - n3*y(x), 0),
                 Eq(n1*y(x).diff(x, x) - n3*y(x), 0),
                 Eq(n1*y(x).diff(x, x) + n3*y(x), 0),
                 ]
    expression = (random.choice(chapter))
    return (expression)

def solve_diff_eq(expression, answer):
    if str(answer_diff_eq(expression)) == str(answer):
        return True
    else:
        return False

def answer_diff_eq(expression):
    # print(expression, 'This is my expression')
    # answer = dsolve(getattr(expression), y())
    answer = dsolve(eval(expression), y(x))
    return answer
