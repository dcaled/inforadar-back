import numpy as np

from .metric import Metric
from scipy import spatial
from gensim.models import KeyedVectors


class HeadlineAccuracyMetric(Metric):

    def __init__(self, pretrained_embeddings_path):
        super().__init__()
        self.word_embeddings_model = KeyedVectors.load_word2vec_format(pretrained_embeddings_path,
                                                                       binary=False,
                                                                       limit=None)

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
        text_embeddings = np.vstack(text_embeddings)
        mean_embeddings_vector = np.mean(text_embeddings, axis=0)
        return mean_embeddings_vector

    def compute_metric(self, headline, body_text):
        """
        Returns the cosine similarity between the word embeddings representation of the article headline and body text.
        """

        headline_embeddings = self.text2vec(headline)
        body_text_embeddings = self.text2vec(body_text)
        cosine_similarity = 1 - spatial.distance.cosine(headline_embeddings, body_text_embeddings)
        return cosine_similarity
