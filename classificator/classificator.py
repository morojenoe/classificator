from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


class ACMClassificator:
    def __init__(self):
        self.rf = RandomForestClassifier()

    def prepare_problems(self, problems):
        return CountVectorizer().fit_transform(p.statement for p in problems)

    def fit(self, problems, tags):
        mat = self.prepare_problems(problems)
        self.rf.fit(mat.toarray(), tags)

    def predict(self, problems):
        mat = self.prepare_problems(problems)
        return self.rf.predict(mat.toarray())
