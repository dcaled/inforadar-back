import numpy as np

from .metric import Metric
from scipy import spatial


class HeadlineAccuracyMetric(Metric):

    def __init__(self, word_embeddings_model):
        super().__init__()
        self.word_embeddings_model = word_embeddings_model

    def create_lexicon(self, raw_file_path):
        pass

    def text2vec(self, text_as_list):
        """
        Input: text, i.e., a list of words.
        Retrieves the vector representation (weights) for each word in text;
        Returns the average weight vector for text's words.
        """
        text_embeddings = []
        for word in text_as_list:
            try:
                word_embeddings = self.word_embeddings_model[word]
                text_embeddings += [word_embeddings]
            except KeyError:
                continue

        # If there's no embedding vector for the words in text, returns None.
        if not text_embeddings:
            return None
        text_embeddings = np.vstack(text_embeddings)
        mean_embeddings_vector = np.mean(text_embeddings, axis=0)
        return mean_embeddings_vector

    def compute_metric(self, headline, body_text):
        """
        Returns the cosine similarity between the word embeddings representation of the article headline and body text.
        """
        cosine_similarity = 0
        headline_embeddings = self.text2vec(headline)
        body_text_embeddings = self.text2vec(body_text)
        if headline_embeddings is not None and body_text_embeddings is not None:
            cosine_similarity = 1 - spatial.distance.cosine(headline_embeddings, body_text_embeddings)
        return cosine_similarity
