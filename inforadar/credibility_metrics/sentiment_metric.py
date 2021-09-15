import codecs
from .metric import Metric


class SentimentMetric(Metric):

    def __init__(self):
        super().__init__()

    def create_lexicon(self, raw_file_path):
        self.lexicon = self.create_sentilex(raw_file_path)

    @staticmethod
    def replace_spaces(term):
        return term.replace(" ", "_")

    @staticmethod
    def __assign_polarity(sent, term, lex):
        if sent == 1:
            lex['POSITIVO'] += [term]
        elif sent == -1:
            lex['NEGATIVO'] += [term]
        else:
            lex['NEUTRO'] += [term]
        return lex

    def create_oplexicon(self, raw_file_path):
        """
        Load valence emotions from oplexicon.
        NEUTRAL | POSITIVE | NEGATIVE.
        """

        spacy_conv = {
            'adj': 'ADJ',
            'n': 'NOUN',
            'vb': 'VERB',
            'det': 'DET',
            'emot': 'EMOT',
            'htag': 'HTAG'
        }

        lex = {
            'POSITIVO': [],
            'NEGATIVO': [],
            'NEUTRO': [],
        }
        with codecs.open(raw_file_path, 'r', 'UTF-8') as hf:
            lines = hf.readlines()
            for line in lines:
                info = line.lower().split(',')
                # if len(info[0].split()) <= 1:
                info[0] = info[0].replace('=', ' ')
                info[1] = [spacy_conv.get(tag) for tag in info[1].split()]
                term, tags, sent = info[:3]
                if 'HTAG' not in tags and 'EMOT' not in tags:
                    term = self.replace_spaces(term.lower().strip())
                    lex = self.__assign_polarity(int(sent), term, lex)

        lex['POSITIVO'] = sorted(list(set(lex['POSITIVO'])))
        lex['NEGATIVO'] = sorted(list(set(lex['NEGATIVO'])))
        lex['NEUTRO'] = sorted(list(set(lex['NEUTRO'])))
        return lex

    def create_sentilex(self, raw_file_path):
        """
        Load valence emotions from sentilex.
        NEUTRAL | POSITIVE | NEGATIVE.
        """

        lex = {
            'POSITIVO': [],
            'NEGATIVO': [],
            'NEUTRO': [],
        }
        with codecs.open(raw_file_path, 'r', 'UTF-8') as hf:
            lines = hf.readlines()
            for line in lines:
                info = line.lower().split('.')
                terms = [term.strip() for term in info[0].split(',')]
                for term in terms:
                    term = self.replace_spaces(term)
                    clex = info[1].split(';')
                    if len(clex) > 0:
                        sent0 = [int(k.replace('pol:n0=', '')) for k in clex if 'pol:n0=' in k]
                        sent1 = [int(k.replace('pol:n1=', '')) for k in clex if 'pol:n1=' in k]

                        # Ignore terms with no n0 (sent0 = []).
                        if not sent0:
                            pass
                        # If not n1, assign n0 polarity.
                        elif len(sent0) == 1 and sent1 == []:
                            lex = self.__assign_polarity(sent0[0], term, lex)
                        # If equal polarities, assign any.
                        elif sent0 == sent1:
                            lex = self.__assign_polarity(sent0[0], term, lex)
                        # If opposing polarities, ignore the term.
                        else:
                            pass

        lex['POSITIVO'] = sorted(list(set(lex['POSITIVO'])))
        lex['NEGATIVO'] = sorted(list(set(lex['NEGATIVO'])))
        lex['NEUTRO'] = sorted(list(set(lex['NEUTRO'])))
        return lex

    def extend_with_oplexicon(self, raw_file_path):
        """ Extends sentilex with new terms from oplexicon. """

        oplexicon = self.create_oplexicon(raw_file_path)

        oplexicon_terms = set(oplexicon['POSITIVO'] + oplexicon['NEUTRO'] + oplexicon['NEGATIVO'])
        sentilex_terms = set(self.lexicon['POSITIVO'] + self.lexicon['NEUTRO'] + self.lexicon['NEGATIVO'])
        missing_terms = list(oplexicon_terms - sentilex_terms)

        for term in missing_terms:
            if term in oplexicon['POSITIVO']:
                self.lexicon['POSITIVO'] += [term]
            elif term in oplexicon['NEUTRO']:
                self.lexicon['NEUTRO'] += [term]
            elif term in oplexicon['NEGATIVO']:
                self.lexicon['NEGATIVO'] += [term]

    def __compute_positive_terms(self, terms):
        """Number of potentially positive terms over the number of terms."""

        n_pos = 0
        for term in terms:
            if term in self.lexicon['POSITIVO']:
                n_pos += 1
        return n_pos

    def __compute_negative_terms(self, terms):
        """Number of potentially negative terms over the number of terms."""

        n_neg = 0
        for term in terms:
            if term in self.lexicon['NEGATIVO']:
                n_neg += 1
        return n_neg

    def __compute_positive_contrast(self, terms):
        """Number of sequences where a positive term (unigram) is followed by a negative term."""

        n_pos_contrast = 0
        for i in range(len(terms) - 1):
            if terms[i] in self.lexicon['POSITIVO'] and terms[i + 1] in self.lexicon['NEGATIVO']:
                # print(terms[i], terms[i+1])
                n_pos_contrast += 1
        return n_pos_contrast

    def __compute_negative_contrast(self, terms):
        """Number of sequences where a negative term (unigram) is followed by a positive term."""

        n_neg_contrast = 0
        for i in range(len(terms) - 1):
            if terms[i] in self.lexicon['NEGATIVO'] and terms[i + 1] in self.lexicon['POSITIVO']:
                # print(terms[i], terms[i+1])
                n_neg_contrast += 1
        return n_neg_contrast

    def compute_metric(self, text_as_list):
        """
        Returns the score of sentiment computed:
        sentiment_ratio = number of sentiment words over divided by the number of terms.
        positive (negative) ratio = number of positive (negative) terms divided by the number of terms.
        positive (negative) contrast = number of positive (negative) contrast divided by the number of sentiment terms.

        Future improvements:
        1. Find the best way to compute the score.
        2. Integrate Portuguese lexica (e.g., OpLexicon).
        """

        n_terms = len(text_as_list)
        n_positive = self.__compute_positive_terms(text_as_list)
        n_negative = self.__compute_negative_terms(text_as_list)
        n_sentiment = n_positive + n_negative

        # metrics = {
        #     'sentiment_ratio': n_sentiment/n_terms,
        #     'positive_ratio': n_positive/n_terms,
        #     'negative_ratio': n_negative/n_terms,
        #     'positive_contrast': self.__compute_positive_contrast(text_as_list)/n_sentiment,
        #     'negative_contrast': self.__compute_negative_contrast(text_as_list)/n_sentiment
        # }
        # return metrics
        return n_sentiment/n_terms
