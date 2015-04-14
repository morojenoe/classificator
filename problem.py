class Problem:
    def __init__(self, statement, submits=None):
        self.submits = [] if submits is None else submits
        self.statement = statement
