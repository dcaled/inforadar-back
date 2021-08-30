import nltk
import pickle
from abc import ABC, abstractmethod


class Metric(ABC):
    def __init__(self):
        self.lexicon = None
        self.stemmer = nltk.stem.SnowballStemmer('portuguese')

    @abstractmethod
    def create_lexicon(self, raw_file_path):
        pass

    @abstractmethod
    def compute_metric(self, text_as_list):
        pass

    def load_lexicon(self, filepath):
        with open(filepath, 'rb') as f:
            self.lexicon = pickle.load(f)

    def save_lexicon(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.lexicon, f)

    def term_to_stem(self, term):
        tokens = term.split(" ")
        tokens = [self.stemmer.stem(tok) for tok in tokens]
        return "_".join(tokens)
