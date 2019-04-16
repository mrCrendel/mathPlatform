import requests
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from process.math.math_simplemath import *
from process.math.math_differential_equation import *
from process.math.math_differantial_equation_with import *
from process.math.math_derivative import *
from process.math.math_integral import *
from process.math.math_limit import *
# from main.settings import GITHUB_USERNAME, GITHUB_TOKEN


class ProgressBar:
    def __init__(self, index, count):
        self.index = index + 1
        self.count = count
        self.progress = round((index + 1) / count * 100)


# @mark_safe
# def markdown_to_html(markdown):
#     url = 'https://api.github.com/markdown'
#     r = requests.post(url, json={"text": markdown}, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
#     if r.status_code == 200:
#         return r.content
#     else:
#         return markdownify(markdown).replace("<code>python", "<code>", 1)


def questions_t_o_f(function_code, question, answer):
    if TopicList.is_addition(function_code) or TopicList.is_subtraction(function_code) or \
                                              TopicList.is_multiplication(function_code) or \
                                              TopicList.is_division(function_code):
        topic_answer = solve_simple_exercise(question, answer, function_code)
    elif TopicList.is_differential_equation(function_code):
        topic_answer = null_answer_diff_eq(question, answer)
    elif TopicList.is_differential_equation_with(function_code):
        topic_answer = null_answer_diff_eq_with(question, answer)
    elif TopicList.is_integral(function_code):
        topic_answer = null_answer_int_eq(question, answer)
    elif TopicList.is_limit(function_code):
        topic_answer = null_answer_lim_eq(question, answer)
    elif TopicList.is_derivative(function_code):
        topic_answer = null_answer_der_eq(question, answer)

    return topic_answer


def question_solver(function_code, question):
    topic_answer = 0

    if TopicList.is_addition(function_code):
        nums = parse_simple_operations(question, '+')
        topic_answer = nums[0] + nums[1]

    elif TopicList.is_subtraction(function_code):
        nums = parse_simple_operations(question, '-')
        topic_answer = nums[0] - nums[1]

    elif TopicList.is_multiplication(function_code):
        nums = parse_simple_operations(question, '*')
        topic_answer = nums[0] * nums[1]

    elif TopicList.is_division(function_code):
        nums = parse_simple_operations(question, '/')
        topic_answer = nums[0] / nums[1]

    elif TopicList.is_differential_equation(function_code):
        topic_answer = solve_diff_eq(question)

    elif TopicList.is_differential_equation_with(function_code):
        topic_answer = solve_diff_eq_with(question)

    elif TopicList.is_integral(function_code):
        topic_answer = solve_int_eq(question)

    elif TopicList.is_limit(function_code):
        topic_answer = solve_lim_eq(question)

    elif TopicList.is_derivative(function_code):
        topic_answer = solve_der_eq(question)

    return topic_answer


def question_creater(function_code):
    if TopicList.is_addition(function_code):
        generated_question = generate_simple_exercise('+')

    elif TopicList.is_subtraction(function_code):
        generated_question = generate_simple_exercise('-')

    elif TopicList.is_multiplication(function_code):
        generated_question = generate_simple_exercise('*')

    elif TopicList.is_division(function_code):
        generated_question = generate_simple_exercise('/')

    elif TopicList.is_differential_equation(function_code):
        generated_question = generate_diff_eq()

    elif TopicList.is_differential_equation_with(function_code):
        generated_question = generate_diff_eq_with()

    elif TopicList.is_integral(function_code):
        generated_question = generate_int_eq()

    elif TopicList.is_limit(function_code):
        generated_question = generate_lim_eq()

    elif TopicList.is_derivative(function_code):
        generated_question = generate_der_eq()

    return generated_question


def convert_to_latex(function_code, question):
    if TopicList.is_differential_equation_with(function_code):
        latex_question = latex(question[0])
    elif TopicList.is_addition(function_code):
        latex_question = latex(question)
    elif TopicList.is_multiplication(function_code):
        latex_question = latex(question)
    elif TopicList.is_subtraction(function_code):
        latex_question = latex(question)
    elif TopicList.is_division(function_code):
        latex_question = latex(question)
    elif TopicList.is_differential_equation(function_code):
        latex_question = latex(question)
    else:
        latex_question = latex(eval(question))
    return latex_question
