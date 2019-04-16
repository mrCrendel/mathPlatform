class TopicList:
    def __init__(self):
        pass

    @staticmethod
    def is_addition(name):
        return "ADDITION" == name.upper()

    @staticmethod
    def is_subtraction(name):
        return "SUBTRACTION" == name.upper()

    @staticmethod
    def is_multiplication(name):
        return "MULTIPLICATION" == name.upper()

    @staticmethod
    def is_division(name):
        return "DIVISION" == name.upper()

    @staticmethod
    def is_differential_equation(name):
        return "DIFF_EQ" == name.upper()

    @staticmethod
    def is_differential_equation_with(name):
        return "DIFF_EQ_WITH_INITIAL_VAL" == name.upper()

    @staticmethod
    def is_integral(name):
        return "INTEGRAL" == name.upper()

    @staticmethod
    def is_limit(name):
        return "LIMIT" == name.upper()

    @staticmethod
    def is_limit_2_1(name):
        return "LIMIT21" == name.upper()

    @staticmethod
    def is_derivative(name):
        return "DERIVATIVE" == name.upper()
