from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
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
        self.mlb = MultiLabelBinarizer()
        self.classificator = OneVsRestClassifier(SVC(), n_jobs=-1)

    def _prepare_problems(self, problems):
        return self.vectorizer.transform([p.statement for p in problems])

    def fit(self, problems, tags):
        nltk.download('punkt', quiet=True)
        self.vectorizer.fit([p.statement for p in problems])
        mat = self._prepare_problems(problems)
        self.mlb = self.mlb.fit(tags)
        self.classificator.fit(mat.toarray(), self.mlb.transform(tags))

    def predict(self, problems):
        mat = self._prepare_problems(problems)
        predicted = self.classificator.predict(mat.toarray())
        return self.mlb.inverse_transform(predicted)


if __name__ == '__main__':
    from main import main

    main(ACMClassificator())
