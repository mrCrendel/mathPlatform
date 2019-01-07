class TopicList:
    def __init__(self):
        pass

    @staticmethod
    def is_six_one(topic_code):
        return "SIX_ONE" == topic_code.upper()

    @staticmethod
    def is_simple_qe(topic_code):
        return "SIMPLE_QE" == topic_code.upper()

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
