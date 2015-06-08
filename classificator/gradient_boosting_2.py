from sklearn.ensemble import GradientBoostingClassifier
import nltk

from base_classificator import BaseACMClassificator
from vectorizer import MyVectorizer


class ACMClassificator(BaseACMClassificator):
    def __init__(self):
        self.vectorizer = MyVectorizer()
        self.classificator = GradientBoostingClassifier(n_estimators=5, learning_rate=0.01, max_features="auto")

    def _prepare_problems(self, problems):
        return self.vectorizer.transform([p.statement for p in problems])

    def fit(self, problems, tags):
        nltk.download('punkt', quiet=True)
        self.vectorizer.fit([p.statement for p in problems])
        mat = self._prepare_problems(problems)
        self.classificator.fit(mat, tags)

    def predict(self, problems):
        mat = self._prepare_problems(problems)
        return self.classificator.predict(mat)


if __name__ == '__main__':
    from main import main

    main(ACMClassificator())
