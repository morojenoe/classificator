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

    def __hash__(self):
        return hash((self.link, self.statement))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.link == other.link and self.statement == other.statement
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return False
