import nltk
from nltk.stem.snowball import EnglishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2


def stem_tokens(tokens, stemmer):
    return [stemmer.stem(item) for item in tokens]


def tokenize(text):
    return stem_tokens(nltk.word_tokenize(text, language='english'), EnglishStemmer())


class MyVectorizer:
    def __init__(self):
        self.tfid_vectorizer = TfidfVectorizer(min_df=0.01, max_df=0.45, tokenizer=tokenize)
        self.k_best = SelectKBest(score_func=chi2, k=256)

    def fit(self, raw_documents, y=None):
        self.k_best.fit(self.tfid_vectorizer.fit_transform(raw_documents), y)

    def transform(self, raw_documents):
        return self.k_best.transform(self.vectorizer.transform(raw_documents))
