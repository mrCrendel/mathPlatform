from sympy import *
import random

x, y, z, u = symbols('x y z u')


def generate_int_eq():
    [a, b, c, d, e, f] = [random.randint(1, 15) for j in range(6)]

    questions = [a,
                 b*x**2,
                 sqrt(a*x),
                 x**b,
                 x**d,
                 (a*x+cos(b*x)),
                 a**2-c*x**2,
                 a+b*x+c*x**2,
                 d*x**(1/2)+b*x**(1/3),
                 (x-b)/x,
                 b*x**3/a-e*x**2/c+a*x-b,
                 a+x**b+x**c+x**d+x**e,
                 cos(b*x),
                 sin(x/a),
                 1/(d+x*c)**2,
                 sqrt(a*x+b),
                 d/(sqrt(a*x+c)),
                 ]
    # print(questions)
    expression = Integral(random.choice(questions), x)
    return expression


def solve_int_eq(expression):
    # print(expression, 'This is my expression')
    # answer = dsolve(getattr(expression), y())
    # expression = get_expression(expression)
    answer = integrate(expression, x)
    return answer


def null_answer_int_eq(expression, answer):
    if str(solve_int_eq(expression)) == str(answer):
        return True
    else:
        return False
