import inforadar.config as config
from inforadar.article import Article
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


def compute_spell_checking_article(content):
    spell_checking_metric = SpellCheckingMetric()
    score = spell_checking_metric.compute_metric(text_as_list=content)
    return score


def insert_article_metrics_scores(id_article, metric_id, score):
    corpus_metric_score = CorpusMetricScore(
        corpus_article_id=id_article,
        metric_id=metric_id,
        score=score
    )
    config.db.session.add(corpus_metric_score)
    config.db.session.commit()


def main():
    path_to_sentiment_lexicon = "path_to_sentiment_lexicon.pkl"
    path_to_subjectivity_lexicon = "path_to_subjectivity_lexicon.pkl "

    metrics = {
        1: "sentiment",
        2: "subjectivity",
        3: "spell_checking"
    }

    corpus = CorpusArticle.query.with_entities(CorpusArticle.id, CorpusArticle.headline, CorpusArticle.body_text)

    for corpus_article in corpus:
        print(corpus_article.id)

        article = Article(corpus_article.headline, corpus_article.body_text, n_grams=1)
        content = article.headline_as_list + article.body_as_list
        content_stems = article.headline_stems + article.body_stems

        sentiment_score = compute_sentiment_article(path_to_sentiment_lexicon, content)
        insert_article_metrics_scores(corpus_article.id, 1, sentiment_score)

        subjectivity_score = compute_subjectivity_article(path_to_subjectivity_lexicon, content_stems)
        insert_article_metrics_scores(corpus_article.id, 2, subjectivity_score)

        spell_checking_score = compute_spell_checking_article(content)
        insert_article_metrics_scores(corpus_article.id, 3, spell_checking_score)


if __name__ == '__main__':
    main()
