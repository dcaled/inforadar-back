import sys

import numpy as np
from gensim.models import KeyedVectors
from scipy import spatial

import inforadar.config as config
from inforadar.article import Article
from inforadar.credibility_metrics.clickbait_metric import ClickbaitMetric
from inforadar.credibility_metrics.sentiment_metric import SentimentMetric
from inforadar.credibility_metrics.spell_checking_metric import SpellCheckingMetric
from inforadar.credibility_metrics.subjectivity_metric import SubjectivityMetric
from inforadar.models import CorpusArticle, CorpusMetricScore


def compute_sentiment_article(fp_lex_sent, content):
    sentiment_metric = SentimentMetric()
    sentiment_metric.load_lexicon(fp_lex_sent)
    score = sentiment_metric.compute_metric(text_as_list=content)
    return score


def compute_subjectivity_article(fp_lex_subj, content_stems):
    subjectivity_metric = SubjectivityMetric()
    subjectivity_metric.load_lexicon(fp_lex_subj)
    score = subjectivity_metric.compute_metric(text_as_list=content_stems)
    return score


def compute_spell_checking_article(fp_extended_vocabulary, content):
    spell_checking_metric = SpellCheckingMetric()
    spell_checking_metric.load_lexicon(fp_extended_vocabulary)
    score = spell_checking_metric.compute_metric(text_as_list=content)
    return score


def compute_clickbait_headline(fp_clickbait_vectorizer, fp_clickbait_model, headline):
    clickbait_metric = ClickbaitMetric(fp_clickbait_vectorizer, fp_clickbait_model)
    score = clickbait_metric.compute_metric(headline)
    return score


def text2vec(word_embeddings_model, text_as_list):
    text_embeddings = []
    for word in text_as_list:
        try:
            word_embeddings = word_embeddings_model[word]
            text_embeddings += [word_embeddings]
        except KeyError:
            continue

    # If there's no embedding vector for the words in text, returns None.
    if not text_embeddings:
        return None
    text_embeddings = np.vstack(text_embeddings)
    mean_embeddings_vector = np.mean(text_embeddings, axis=0)
    return mean_embeddings_vector


def compute_headline_accuracy_article(word_embeddings_model, headline_as_list, body_as_list):
    score = 0
    headline_embeddings = text2vec(word_embeddings_model, headline_as_list)
    body_text_embeddings = text2vec(word_embeddings_model, body_as_list)
    if headline_embeddings is not None and body_text_embeddings is not None:
        score = 1 - spatial.distance.cosine(headline_embeddings, body_text_embeddings)
    return score


def insert_article_metrics_scores(id_article, metric_id, score, version):
    corpus_metric_score = CorpusMetricScore(
        corpus_article_id=id_article,
        metric_id=metric_id,
        score=score,
        version=version
    )
    config.db.session.add(corpus_metric_score)
    config.db.session.commit()


def main():
    path_to_sentiment_lexicon = "path_to_sentiment_lexicon.pkl"
    path_to_subjectivity_lexicon = "path_to_subjectivity_lexicon.pkl"
    path_to_embedding_weights = "path_to_cbow_s300.txt"
    path_to_clickbait_vectorizer = 'path_to_clickbait_vectorizer.pk'
    path_to_clickbait_model = 'path_to_clickbait_model.sav'
    path_to_extended_vocabulary = 'path_to_extended_vocabulary.pkl'

    # word_embeddings_model = KeyedVectors.load_word2vec_format(path_to_embedding_weights,
    #                                                           binary=False,
    #                                                           limit=None)
    metrics = {
        1: "sentiment",
        2: "subjectivity",
        3: "spell_checking",
        5: "headline_accuracy"
    }

    corpus = CorpusArticle.query.with_entities(CorpusArticle.id, CorpusArticle.headline, CorpusArticle.body_text)

    for corpus_article in corpus:
        print(corpus_article.id)

        article = Article(corpus_article.headline, corpus_article.body_text, n_grams=1)
        content = article.headline_as_list + article.body_as_list
        content_stems = article.headline_stems + article.body_stems

        # Sentiment
        # sentiment_score = compute_sentiment_article(path_to_sentiment_lexicon, content)
        # insert_article_metrics_scores(corpus_article.id, 1, sentiment_score, 1)

        # Subjectivity
        # subjectivity_score = compute_subjectivity_article(path_to_subjectivity_lexicon, content_stems)
        # insert_article_metrics_scores(corpus_article.id, 2, subjectivity_score, 1)

        # Spell checking
        spell_checking_score = compute_spell_checking_article(path_to_extended_vocabulary, content)
        # print(spell_checking_score)
        insert_article_metrics_scores(corpus_article.id, 3, spell_checking_score, 2)

        # Clickbait headline
        # clickbait_headline_score = compute_clickbait_headline(path_to_clickbait_vectorizer,
        #                                                       path_to_clickbait_model,
        #                                                       article.headline)
        # insert_article_metrics_scores(corpus_article.id, 4, clickbait_headline_score, 1)
        # print(article.headline, clickbait_headline_score)

        # Headline accuracy
        # headline_accuracy_score = compute_headline_accuracy_article(word_embeddings_model,
        #                                                             article.headline_as_list,
        #                                                             article.body_as_list[:100])
        # insert_article_metrics_scores(corpus_article.id, 5, headline_accuracy_score, 1)
        # print(headline_accuracy_score)


if __name__ == '__main__':
    main()
