class Solution:
    cpp_lang = 'C++'
    java_lang = 'Java'

    def __init__(self, code, language):
        self.code = code
        self.language = language


class Problem:
    def __init__(self, statement, link, solutions=None):
        self.solutions = [] if solutions is None else solutions
        self.statement = statement
        self.link = link
