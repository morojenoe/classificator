class Solution:
    cpp_lang = 'C++'
    java_lang = 'Java'

    def __init__(self, code, language):
        self.code = code
        self.language = language


class Problem:
    def __init__(self, statement, link, solution=None):
        self.solutions = [] if solution is None else solution
        self.statement = statement
        self.link = link
