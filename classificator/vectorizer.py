import nltk
from nltk.stem.snowball import EnglishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


def stem_tokens(tokens, stemmer):
    return [stemmer.stem(item) for item in tokens]


def tokenize(text):
    return stem_tokens(nltk.word_tokenize(text, language='english'), EnglishStemmer())


class MyVectorizer:
    def __init__(self):
        self.tfid_vectorizer = TfidfVectorizer(min_df=0.01, max_df=0.45, tokenizer=tokenize)

    def fit(self, raw_documents):
        self.tfid_vectorizer.fit_transform(raw_documents)

    def transform(self, raw_documents):
        return self.tfid_vectorizer.transform(raw_documents)
