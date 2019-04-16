import random
from sympy import *

y = Function('y')
x = Symbol('x',  real=True)


def generate_diff_eq_with():
    a = random.randint(1, 15)
    b = random.randint(1, 15)
    c = random.randint(1, 15)
    n1 = random.randint(-10, 10)
    n2 = random.randint(-10, 10)

    questions = [Eq(a*y(x).diff(x, x) + b*y(x).diff(x) + c*y(x), 0),
                 Eq(a*y(x).diff(x, x) - b*y(x).diff(x) - c*y(x), 0),
                 Eq(a*y(x).diff(x, x) - b*y(x).diff(x), 0),
                 Eq(a*y(x).diff(x, x) + b*y(x).diff(x), 0),
                 Eq(a*y(x).diff(x, x) - b*y(x).diff(x) + c*y(x), 0),
                 Eq(a*y(x).diff(x, x) + b*y(x).diff(x) - c*y(x), 0),
                 Eq(a*y(x).diff(x, x) - b*y(x), 0),
                 Eq(a*y(x).diff(x, x) + b*y(x), 0),
                 Eq(a * diff(y(x), x, 2) + b * diff(y(x), x) - c * y(x), 0),
                 Eq(diff(y(x), x, 2) + a * diff(y(x), x) + c * y(x), 0),
                 Eq(diff(y(x), x, 2) + a * diff(y(x), x), 0),
                 Eq(diff(y(x), x, 2) + diff(y(x), x), 0),
                 ]
    expression = [random.choice(questions), n1, n2]
    return expression


def solve_diff_eq_with(eq):
    eq = eval(eq)
    y0 = eq[1]
    y1 = eq[2]
    eq = eq[0]
    # print(expression, 'This is my expression')
    # answer = dsolve(getattr(expression), y())
    y_sl0 = dsolve(eq, y(x)).rhs # take only right hand side
    cnd0 = Eq(y_sl0.subs(x, 0), y0)  # y(0) = n1
    cnd1 = Eq(y_sl0.diff(x).subs(x, 0), y1)  # y'(0) = n2

    #  Solve for C1, C2:
    C1, C2 = symbols("C1, C2")  # generic constants
    C1C2_sl = solve([cnd0, cnd1], (C1, C2))

    # Substitute back into solution:
    y_sl1 = simplify(y_sl0.subs(C1C2_sl))
    answer = dsolve(eq, y(x))

    # answer = dsolve(eval(expression), y(x))
    return answer


def null_answer_diff_eq_with(expression, answer):
    if str(solve_diff_eq_with(expression)) == str(answer):
        return True
    else:
        return False
