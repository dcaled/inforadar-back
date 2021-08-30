from pprint import pprint
import unicodedata
import nltk
from nltk.tokenize import RegexpTokenizer


class Article:
    def __init__(self, headline, body, n_grams=1):
        self.headline = headline.strip()
        self.body = body.strip()

        self.headline_as_list = self.preprocess(self.headline)
        self.body_as_list = self.preprocess(self.body)

        self.headline_ngrams = self.get_ngrams(self.headline_as_list, n_grams)
        self.body_ngrams = self.get_ngrams(self.body_as_list, n_grams)

        self.stemmer = nltk.stem.SnowballStemmer('portuguese')
        self.headline_stems = [self.term_to_stem(term) for term in self.headline_as_list]
        self.body_stems = [self.term_to_stem(term) for term in self.body_as_list]

        self.headline_stems_ngrams = self.get_ngrams(self.headline_stems, n_grams)
        self.body_stems_ngrams = self.get_ngrams(self.body_stems, n_grams)

    def print(self):
        pprint(self.__dict__)

    def preprocess(self, text):
        text = unicodedata.normalize('NFC', text)
        tokenizer = RegexpTokenizer(r'[\w\-]+')
        terms = tokenizer.tokenize(text.lower())
        return terms

    def term_to_stem(self, term):
        return self.stemmer.stem(term)

    def get_ngrams(self, terms, n_grams):
        if n_grams > 3:
            print('Invalid n_grams value. This method is limited to trigrams (n_grams=3).')
            return []

        if n_grams == 2:
            terms += self.extract_bigrams(terms)
        elif n_grams == 3:
            bigrams = self.extract_bigrams(terms)
            trigrams = self.extract_trigrams(terms)
            terms += bigrams + trigrams
        return terms

    @staticmethod
    def extract_bigrams(terms):
        bigrams = list(nltk.bigrams(terms))
        bigrams = ['_'.join(bigram) for bigram in bigrams]
        return bigrams

    @staticmethod
    def extract_trigrams(terms):
        trigrams = list(nltk.trigrams(terms))
        trigrams = ['_'.join(trigram) for trigram in trigrams]
        return trigrams
