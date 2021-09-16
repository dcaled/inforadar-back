from spellchecker import SpellChecker
from .metric import Metric


class SpellCheckingMetric(Metric):

    def __init__(self):
        super().__init__()
        self.spell_portuguese = SpellChecker(language="pt")
        self.spell_portuguese.word_frequency.load_words(
            ["marcelo", "rebelo", "covid", "covid-19", "oms", "sars-cov", "pfizer",
             "bolsonaro", "covid-19", "https", "huawei", "coronavírus", "5g", "biden", "hidroxicloroquina",
             "lisboa",
             "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"])

    def create_lexicon(self, raw_file_path):
        pass

    def compute_metric(self, text_as_list):
        """
        Returns the typographical error ratio.
        https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/
        https://natura.di.uminho.pt/download/sources/Dictionaries/hunspell/
        https://github.com/barrust/pyspellchecker
        """

        n_terms = len(text_as_list)
        misspelled = self.spell_portuguese.unknown(text_as_list)
        # print(misspelled)

        return len(misspelled)/n_terms
