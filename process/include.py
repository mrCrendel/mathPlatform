import requests
from django import template
from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from process.subject_topic_list import *
from process.subject_simplemath import *
from process.subject_calculus_1 import *
# from main.settings import GITHUB_USERNAME, GITHUB_TOKEN


class ProgressBar:
    def __init__(self, index, count):
        self.index = index + 1
        self.count = count
        self.progress = round((index + 1) / count * 100)


@mark_safe
def markdown_to_html(markdown):
    url = 'https://api.github.com/markdown'
    r = requests.post(url, json={"text": markdown}, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if r.status_code == 200:
        return r.content
    else:
        return markdownify(markdown).replace("<code>python", "<code>", 1)


def questions_t_o_f(function_code, question, answer):
    # get True or False to given question and answer
    if TopicList.is_six_one(function_code):
        topic_answer = solve_six_one(question, answer)
    elif TopicList.is_simple_qe(function_code):
        topic_answer = get_random_result(2)
    elif TopicList.is_addition(function_code) or TopicList.is_subtraction(function_code) or \
                                              TopicList.is_multiplication(function_code) or \
                                              TopicList.is_division(function_code):
        topic_answer = solve_simple_exercise(question, answer, function_code)
    return topic_answer

def question_solver(function_code, question):
    topic_answer = 0
    if TopicList.is_six_one(function_code):
        topic_answer = answer_six_one(question, answer)

    elif TopicList.is_simple_qe(function_code):
        topic_answer = get_random_result(2)

    elif TopicList.is_addition(function_code):
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
    return topic_answer


def question_creater(function_code):
    if TopicList.is_six_one(function_code):
        generated_question = generate_six_one()

    elif TopicList.is_simple_qe(function_code):
        generated_question = generate_simple_qe()

    elif TopicList.is_addition(function_code):
        generated_question = generate_simple_exercise('+')

    elif TopicList.is_subtraction(function_code):
        generated_question = generate_simple_exercise('-')

    elif TopicList.is_multiplication(function_code):
        generated_question = generate_simple_exercise('*')

    elif TopicList.is_division(function_code):
        generated_question = generate_simple_exercise('/')

    return generated_question
