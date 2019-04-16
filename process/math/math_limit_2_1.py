from sympy import *
import random

x, y, z, u = symbols('x y z u')


def generate_lim_2_1_eq():
    a = int(random.randint(1, 15))
    b = int(random.randint(1, 15))
    c = int(random.randint(1, 15))
    d = int(random.randint(1, 15))
    e = int(random.randint(1, 15))
    f = int(random.randint(1, 15))
    i = int(random.randint(-4, 5))

    questions = [Limit(a/x, x, 0, '-'),
                 Limit(x**2 - a*x + b, x, i),
                 Limit((x + a)/(x + b), x, i),
                 Limit((x - a)/(x + b), x, i),
                 Limit((x + a)/(x - b), x, i),
                 Limit((x - a)/(x - b), x, i),
                 Limit((x**2 - a)/(x + b), x, i),
                 Limit((x**2 - a)/(x - b), x, i),
                 Limit((x**2 + a)/(x - b), x, i),
                 Limit((x**2 + a)/(x - b), x, i),
                 Limit(a*(b - x)*(c - x), x, i),
                 Limit(a*(b + x)*(c - x), x, i),
                 Limit(a*(b - x)*(c + x), x, i),
                 Limit(a*(b + x)*(c + x), x, i),
                 Limit(x**2/(a - x), x, i),
                 Limit(x**2/(a + x), x, i),
                 Limit(x**2/(a - x), x, i),



                 ]
    # print(questions)
    expression = random.choice(questions)
    return expression


# def solve_lim_eq(expression):
#     # print(expression, 'This is my expression')
#     # answer = dsolve(getattr(expression), y())
#     # expression = get_expression(expression)
#     answer = eval(expression).doit()
#     return answer
#
#
# def null_answer_lim_eq(expression, answer):
#     if str(solve_lim_eq(expression)) == str(answer):
#         return True
#     else:
#         return False
