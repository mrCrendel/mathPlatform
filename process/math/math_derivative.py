from sympy import *
import random

x, y, z, u = symbols('x y z u')


def get_expression(expression):
    expression = [i for i in str(expression).split(',')][0].replace('Derivative(', '')
    return expression


def generate_der_eq():
    a = int(random.randint(1, 15))
    b = int(random.randint(1, 15))
    c = int(random.randint(1, 15))
    d = int(random.randint(1, 15))
    e = int(random.randint(1, 15))
    f = int(random.randint(1, 15))

    questions = [(a*x+b)**c,
                 (a-x/b)**c,
                 (a-x**b)**c,
                 sqrt(a-b*x**c),
                 (a+b/y)**(-c),
                 (a+x**(b/c))**(c/d),
                 a/(b-x*c),
                 (a-b*y**b)**(-c/b),
                 (a-x**b),
                 (a+y**b),
                 a*x+(b*x-c),
                 (a+x**3)**(b/c),
                 d/(a+sqrt(b*x+c)),
                 (a+sqrt((x-b)/c))**d,
                 (u+a/(u-b))**(-c/d),
                 (x**a*sqrt(b+x**c))/(d+x**e)**f,
                 sqrt(sqrt(x)),
                 sqrt(x*sqrt(x)),
                 sqrt(x**a),
                 sqrt(x**a+sqrt(x+b)),
                 a*x**2-b*x-c,
                 a * x ** (1 / 2) - b / x,
                 a * x ** 2 + b * x + c,
                 a / x ** 3 + b / x ** 2 - c,
                 (x ** 5 - x ** 3) / c,
                 x ** 45 - x ** -45,
                 x ** (1 / 3) + a * x ** (1 / 4) + b * x ** (1 / 5),
                 a * (x ** (2 / 3)) - b / (x ** (3 / 2)),
                 a / b * x ** (5 / 3) - b / a * x ** (-3 / 5),
                 (a * x - b) * (c - d * x),
                 x ** (1 / 2) * (c - x - x ** 2 / f),
                 ]
    expression = Derivative(random.choice(questions))
    return expression


def solve_der_eq(expression):
    # print(expression, 'This is my expression')
    # answer = dsolve(getattr(expression), y())
    expression = get_expression(expression)
    answer = diff(eval(expression))
    return answer


def null_answer_der_eq(expression, answer):
    if str(solve_der_eq(expression)) == str(answer):
        return True
    else:
        return False

