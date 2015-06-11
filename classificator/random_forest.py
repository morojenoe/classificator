from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from .base_classificator import BaseACMClassificator
from nltk.stem.snowball import EnglishStemmer
import nltk


def stem_tokens(tokens, stemmer):
    return [stemmer.stem(item) for item in tokens]


def tokenize(text):
    return stem_tokens(nltk.word_tokenize(text, language='english'), EnglishStemmer())


class ACMClassificator(BaseACMClassificator):
    def __init__(self):
        self.vectorizer = CountVectorizer(min_df=0.05, max_df=0.45, tokenizer=tokenize)
        self.classificator = RandomForestClassifier(n_estimators=256,
                                                    criterion="gini",
                                                    max_depth=None,
                                                    min_samples_split=2,
                                                    min_samples_leaf=1,
                                                    min_weight_fraction_leaf=0.,
                                                    max_features="auto",
                                                    max_leaf_nodes=None,
                                                    bootstrap=True,
                                                    oob_score=False,
                                                    n_jobs=-1,
                                                    class_weight=None)

    def _prepare_problems(self, problems):
        return self.vectorizer.transform([p.statement for p in problems])

    def fit(self, problems, tags):
        nltk.download('punkt', quiet=True)
        self.vectorizer.fit([p.statement for p in problems])
        mat = self._prepare_problems(problems)
        self.classificator.fit(mat.toarray(), tags)

    def predict(self, problems):
        mat = self._prepare_problems(problems)
        return self.classificator.predict(mat.toarray())


if __name__ == '__main__':
    from main import main

    main(ACMClassificator())
