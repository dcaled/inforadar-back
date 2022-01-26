import pickle
import re
import string

import numpy as np

from .metric import Metric


class ClickbaitMetric(Metric):

    def __init__(self, vectorizer_file_path, model_file_path):
        super().__init__()
        self.vectorizer = self.load_vectorizer(vectorizer_file_path)
        self.model = self.load_model(model_file_path)

    def create_lexicon(self, raw_file_path):
        pass

    def clean_text(self, text):
        """Make text lowercase, remove text in square brackets, remove punctuation, and remove words
        containing numbers."""

        text = text.lower()
        text = re.sub("\n", " ", text)
        text = re.sub("  ", " ", text)
        text = re.sub(r"^https?:\/\/.*[\r\n]*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", text)
        text = re.sub("\[.*?\]", " ", text)
        text = re.sub("[%s]" % re.escape(string.punctuation), "", text)
        text = re.sub("“", "", text)
        text = re.sub("”", "", text)
        text = re.sub("’", "", text)
        text = re.sub("–", "", text)
        text = re.sub("‘", "", text)
        return text

    def count_words(self, clean_headline):
        return len(clean_headline.split())

    def contains_exclamation(self, clean_headline):
        if "!" in clean_headline:
            return 1
        return 0

    def contains_question(self, clean_headline):
        if "?" in clean_headline or clean_headline.startswith((
                "quem", "qual", "quais", "quanto", "quantos", "quanta", "quantas", "quando",
                "que ", "como", "onde", "aonde", "cadê",
                "de quem", "de qual", "de quais", "de quanto", "de quantos", "de quanta", "de quantas", "de quando",
                "de que", "de onde",
                "por quem", "por qual", "por quais", "por quanto", "por quantos", "por quanta", "por quantas",
                "por que",
                "por onde",
                "o que", "há quanto")):
            return 1
        return 0

    def starts_with_num(self, clean_headline):
        if clean_headline.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
            return 1
        return 0

    def compute_metric(self, headline):
        features = self.generate_features(headline)
        result = self.model.predict_proba([features])[0][1]
        return result

    def load_vectorizer(self, vectorizer_file_path):
        # print(vectorizer_file_path)
        vectorizer = pickle.load(open(vectorizer_file_path, "rb"))
        return vectorizer

    def load_model(self, model_file_path):
        model = pickle.load(open(model_file_path, "rb"))
        return model

    def generate_features(self, headline):
        """
        Is This Headline Clickbait?: https://towardsdatascience.com/is-this-headline-clickbait-86d27dc9b389
        Is This Headline Clickbait? [code]: https://github.com/AlisonSalerno/clickbait_detector
        """
        clean_headline = self.clean_text(headline)
        headline_words = self.count_words(clean_headline)
        exclamation = self.contains_exclamation(clean_headline)
        question = self.contains_question(clean_headline)
        starts_with_num = self.starts_with_num(clean_headline)

        tfidf = self.vectorizer.transform([clean_headline]).toarray()
        # print(tfidf)
        features = np.hstack((np.array([headline_words, exclamation, starts_with_num, question]), tfidf[0]))
        return features
