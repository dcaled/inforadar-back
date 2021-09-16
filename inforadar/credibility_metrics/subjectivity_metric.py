import csv
from .metric import Metric


class SubjectivityMetric(Metric):
    def __init__(self):
        super().__init__()

    def create_lexicon(self, raw_file_path):
        """
        Recognizing Contextual Polarity in Phrase-Level Sentiment Analysis.
        Theresa Wilson, Janyce Wiebe, and Paul Hoffmann (2005).
        http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
        """

        lex = {'strongsubj': [], 'weaksubj': []}

        with open(raw_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                term = self.term_to_stem(row[3])
                # lex[stem] = {'strongsubj':0, 'weaksubj':0}
                if row[0] == 'strongsubj':
                    lex['strongsubj'] += [term]
                elif row[0] == 'weaksubj':
                    lex['weaksubj'] += [term]

        all_words = list(set(lex['strongsubj'] + lex['weaksubj']))

        for w in all_words:
            if lex['weaksubj'].count(w) > lex['strongsubj'].count(w):
                lex['strongsubj'] = list(filter(w.__ne__, lex['strongsubj']))
            elif lex['weaksubj'].count(w) < lex['strongsubj'].count(w):
                lex['weaksubj'] = list(filter(w.__ne__, lex['weaksubj']))
            else:
                lex['strongsubj'] = list(filter(w.__ne__, lex['strongsubj']))
                lex['weaksubj'] = list(filter(w.__ne__, lex['weaksubj']))

        self.lexicon = lex

    def compute_metric(self, text_as_list, weak_subjectivity=False):
        """
        Returns the score of subjectivity computed as:
        The number of strong or weak subjectivity terms in the document divided by the number of terms in the document.

        Future improvements:
        1. Find the best way to compute the score.
        2. Attribute higher weights to strong subjectivity terms.
        3. Create a portuguese lexicon.
        """

        n_terms_subj = 0
        n_terms = len(text_as_list)
        # subj_feats = {'strongsubj': 0, 'weaksubj': 0}

        for term in text_as_list:
            if term in self.lexicon['strongsubj']:
                # subj_feats['strongsubj'] += 1
                n_terms_subj+=1
            elif weak_subjectivity and (term in self.lexicon['weaksubj']):
                # subj_feats['weaksubj'] += 1
                n_terms_subj+=1

        #subj_feats.update({k: v / n_terms for k, v in subj_feats.items()})
        #return subj_feats
        return n_terms_subj/n_terms
