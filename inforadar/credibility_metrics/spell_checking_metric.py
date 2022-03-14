import pickle

from spellchecker import SpellChecker
from .metric import Metric


class SpellCheckingMetric(Metric):

    def __init__(self):
        super().__init__()
        self.spell_portuguese = SpellChecker(language="pt")

    def load_lexicon(self, filepath):
        with open(filepath, "rb") as f:
            lexicon = pickle.load(f)
            self.lexicon = list(lexicon.keys())

    def create_lexicon(self, raw_file_path):
        pass

    def compute_metric(self, text_as_list):
        """
        Returns the typographical error ratio.
        https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/
        https://natura.di.uminho.pt/download/sources/Dictionaries/hunspell/
        https://github.com/barrust/pyspellchecker
        """

        self.spell_portuguese.word_frequency.load_words(self.lexicon)
        n_terms = len(text_as_list)
        misspelled = self.spell_portuguese.unknown(text_as_list)
        # print(misspelled)

        return len(misspelled) / n_terms
