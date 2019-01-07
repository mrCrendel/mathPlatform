class TopicList:
    def __init__(self):
        pass

    @staticmethod
    def is_six_one(topic_code):
        return "SIX_ONE" == topic_code.upper()

    @staticmethod
    def is_simple_qe(topic_code):
        return "SIMPLE_QE" == topic_code.upper()
