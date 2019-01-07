import random
from process.subject_topic_list import *

def generate_simple_exercise(operation):
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)

    exercise = str(num1) + " " + operation + " " + str(num2) + " = "
    return exercise


def solve_simple_exercise(expression, userAnswer, topic_code):
    result_answer = 0
    if TopicList.is_addition(topic_code):
        nums = parse_simple_operations(expression, '+')
        result_answer = nums[0] + nums[1]

    if TopicList.is_subtraction(topic_code):
        nums = parse_simple_operations(expression, '-')
        result_answer = nums[0] - nums[1]

    if TopicList.is_multiplication(topic_code):
        nums = parse_simple_operations(expression, '*')
        result_answer = nums[0] * nums[1]

    if TopicList.is_division(topic_code):
        nums = parse_simple_operations(expression, '/')
        result_answer = nums[0] / nums[1]

    if is_answers_equal(result_answer, userAnswer):
        return True
    return False


def parse_simple_operations(expression, symbol):
    nums = expression.split(symbol)
    if len(nums) != 2:
        return
    nums[1] = nums[1].replace(' ', '').replace('=', '')
    return [
        float(nums[0].replace(' ', '')),
        float(nums[1].replace(' ', ''))
    ]


def is_answers_equal(var1, var2):
    precision = "{:.2f}"
    return precision.format(float(var1)) == precision.format(float(var2))
