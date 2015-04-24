class Submit:
    def __init__(self, code, language):
        self.code = code
        self.language = language


class Problem:
    def __init__(self, statement, link, submits=None):
        self.submits = [] if submits is None else submits
        self.statement = statement
        self.link = link
