from sympy import *
import random

x, y, z, u = symbols('x y z u')


def generate_lim_eq():
    a = int(random.randint(1, 15))
    b = int(random.randint(1, 15))
    c = int(random.randint(1, 15))
    d = int(random.randint(1, 15))
    e = int(random.randint(1, 15))
    f = int(random.randint(1, 15))

    questions = [Limit(a/x, x, 0, '-'),
                 Limit(x**2/exp(x), x, 0),
                 Limit(x/(a*x-b), x, oo),
                 Limit((a*x**3-b*x**2+c)/(d+e*x-f*x**3), x, oo),
                 Limit((x**2-a)/(x-x**2), x, oo, '-'),
                 Limit((x**2+a)/(x**3+b),x,oo,'-'),
                 Limit((x**2+sin(x))/(x**2+cos(x)),x,oo),
                 Limit((a*x+2*sqrt(x))/(b-x),x,oo),
                 Limit((a*x-c)/sqrt(b*x**2+x+c),x,oo),
                 Limit((a*x-b)/sqrt(c*x**2+x+d),x,oo,'-'),
                 Limit((a*x-b)/abs(c*x+d), x, oo, '-'),
                 Limit(a/(b-x), x, c),
                 Limit(a/(b-x)**2,x,c),
                 Limit(a/(b-x),x,c,'-'),
                 Limit(a/(b-x),x,c,'+'),
                 Limit((a*x+b)/(c*x+d),x,-e/f,'-'),
                 Limit((a*x+b)/(c*x+d),x,-e/f,'+'),
                 Limit(x/(a-x)**3,x,b,'+'),
                 Limit(x/sqrt(a+x**2),x,b,'-'),
                 Limit(x/sqrt(a-x**2),x,b,'+'),
                 ]
    # print(questions)
    expression = random.choice(questions)
    return expression


def solve_lim_eq(expression):
    # print(expression, 'This is my expression')
    # answer = dsolve(getattr(expression), y())
    # expression = get_expression(expression)
    answer = eval(expression).doit()
    return answer


def null_answer_lim_eq(expression, answer):
    if str(solve_lim_eq(expression)) == str(answer):
        return True
    else:
        return False
