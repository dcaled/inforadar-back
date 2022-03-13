from multiprocessing.managers import BaseManager

from cerberus import Validator
from flask import request, g
from flask_restful import Resource

import inforadar.config as config
from inforadar import constants
from inforadar.article import Article
from inforadar.credibility_metrics.headline_accuracy_metric import HeadlineAccuracyMetric
from inforadar.credibility_metrics.sentiment_metric import SentimentMetric
from inforadar.credibility_metrics.spell_checking_metric import SpellCheckingMetric
from inforadar.credibility_metrics.subjectivity_metric import SubjectivityMetric
from inforadar.credibility_metrics.clickbait_metric import ClickbaitMetric
from inforadar.models import Category, Metric, CrowdsourcedArticle, \
    CrowdsourcedMetricScore, MetricPercentile, CorpusMetricScore
from ..constants import current_version_metric_sentiment, current_version_metric_subjectivity, \
    current_version_metric_spell_checking, current_version_metric_headline_accuracy, current_version_metric_clickbait


class Metrics(Resource):

    def get(self):
        """
        Output: dictionary listing each metric, the corresponding description, and the quartiles for each category
        (fact, opinion, conspiracy, entertainment, and satire).
        """

        categories_records = Category.query.with_entities(Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        metrics_records = Metric.query.with_entities(
            Metric.id, Metric.name, Metric.display_name, Metric.description).all()
        available_metrics = {record.id: record.name for record in metrics_records}

        metrics = dict()
        for metric in available_metrics:
            metrics[metric.id] = {
                "id": metric.id,
                "name": metric.name,
                "display_name": metric.display_name,
                "description": metric.description,
                "categories": dict()
            }

            for category in categories:
                metrics[metric.id]["categories"][category.category_id] = {
                    "first_quartile": 25,
                    "second_quartile": 50,
                    "third_quartile": 75,
                    "fourth_quartile": 100
                }

        metrics = list(metrics.values())
        return metrics, 200

    def post(self):
        """
        Input: headline (optional ?), and body text (mandatory), list with metrics.
        Output: a dictionary listing the score and percentile for each category and each metric.
        """

        categories_records = Category.query.with_entities(Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        metrics_records = Metric.query.with_entities(Metric.id, Metric.name).all()
        available_metrics = {record.id: record.name for record in metrics_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        schema_1 = {
            "id": {"type": "integer", "required": True},
            "metrics": {"type": "list",
                        "required": True,
                        "allowed": available_metrics,
                        "schema": {"type": "integer"}
                        },
        }

        schema_2 = {
            "headline": {"type": "string", "required": True},
            "body_text": {"type": "string", "required": True},
            "metrics": {"type": "list",
                        "required": True,
                        "allowed": available_metrics,
                        "schema": {"type": "integer"}
                        },
        }

        validator = Validator()
        valid = any(validator(request.get_json(force=True), schema) for schema in [schema_1, schema_2])
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)
        metrics = dict()
        article_id = None

        # --------------------------
        # Persist article and retrieve existing metrics.
        # --------------------------
        if data.get("id", None):
            # metrics_records = Category.query.with_entities(Metric.id, Metric.name).all()
            article = CrowdsourcedArticle.query.filter_by(id=data["id"]).first()
            if not article:
                return {"message": f"Invalid article id: " + str(data["id"]) + "."}, 400
            headline = article.headline
            body_text = article.body_text

            # TODO: Attention: when a new version of the indicators calculator is released, you should update this
            #  query to retrieve the score of the current indicator calculator.
            metrics_records = CrowdsourcedArticle.query \
                .join(CrowdsourcedMetricScore,
                      CrowdsourcedMetricScore.crowdsourced_article_id == CrowdsourcedArticle.id) \
                .add_columns(CrowdsourcedMetricScore.metric_id, CrowdsourcedMetricScore.score) \
                .filter(CrowdsourcedArticle.id == article.id) \
                .filter(CrowdsourcedMetricScore.metric_id.in_(data["metrics"])).all()

            for record in metrics_records:
                metrics[record.metric_id] = {"score": record.score}
            article_id = article.id

        else:
            headline = data.get("headline", None)
            body_text = data.get("body_text", None)

        # --------------------------
        # Compute score for each metric.
        # --------------------------
        new_metrics = dict()
        for metric_id in data.get("metrics"):
            if metric_id not in metrics.keys():

                art = Article(headline, body_text, n_grams=1)
                content = art.headline_as_list + art.body_as_list
                content_stems = art.headline_stems + art.body_stems

                if available_metrics[metric_id] == "sentiment":
                    sentiment_metric = SentimentMetric()
                    sentiment_metric.load_lexicon(constants.fp_lex_sent)
                    score = sentiment_metric.compute_metric(text_as_list=content)
                    new_metrics[metric_id] = {
                        "score": score,
                        "version": current_version_metric_sentiment
                    }

                elif available_metrics[metric_id] == "subjectivity":
                    subjectivity_metric = SubjectivityMetric()
                    subjectivity_metric.load_lexicon(constants.fp_lex_subj)
                    score = subjectivity_metric.compute_metric(text_as_list=content_stems)
                    new_metrics[metric_id] = {
                        "score": score,
                        "version": current_version_metric_subjectivity
                    }

                elif available_metrics[metric_id] == "spell_checking":
                    spell_checking_metric = SpellCheckingMetric()
                    score = spell_checking_metric.compute_metric(text_as_list=content)
                    new_metrics[metric_id] = {
                        "score": score,
                        "version": current_version_metric_spell_checking
                    }

                elif available_metrics[metric_id] == "headline_accuracy":
                    if not headline:
                        score = None
                        message = "Error when computing headline_accuracy. No headline provided."
                        new_metrics[metric_id] = {"score": score, "message": message}
                    elif not body_text:
                        score = None
                        message = "Error when computing headline_accuracy. No body text provided."
                        new_metrics[metric_id] = {"score": score, "message": message}
                    else:
                        BaseManager.register("create_embedding_matrix")
                        manager = BaseManager(address=('localhost', 5001), authkey=b'pass')
                        manager.connect()
                        word_embeddings_model = manager.create_embedding_matrix(
                            constants.fp_emb_matrix,
                            embedding_dim=300)._getvalue()
                        headline_accuracy_metric = HeadlineAccuracyMetric(word_embeddings_model)
                        score = headline_accuracy_metric.compute_metric(headline=art.headline_as_list,
                                                                        body_text=art.body_as_list[:100])
                        new_metrics[metric_id] = {
                            "score": score,
                            "version": current_version_metric_headline_accuracy
                        }
                elif available_metrics[metric_id] == "clickbait":
                    if not headline:
                        score = None
                        message = "Error when computing clickbait. No headline provided."
                        new_metrics[metric_id] = {"score": score, "message": message}
                    else:
                        clickbait_metric = ClickbaitMetric(
                            constants.fp_clickbait_vectorizer,
                            constants.fp_clickbait_model)
                        score = clickbait_metric.compute_metric(headline)
                        new_metrics[metric_id] = {
                            "score": score,
                            "version": current_version_metric_clickbait
                        }

                # print(new_metrics)

        metrics.update(new_metrics)

        # --------------------------
        # Persist new metrics.
        # --------------------------
        if article_id:
            for metric_id, values in new_metrics.items():
                if values["score"] is not None:
                    metric_score = CrowdsourcedMetricScore(metric_id=metric_id,
                                                           crowdsourced_article_id=article_id,
                                                           score=new_metrics[metric_id]["score"],
                                                           version=new_metrics[metric_id]["version"]
                                                           )
                    config.db.session.add(metric_score)
                    config.db.session.commit()

        # --------------------------
        # Get percentiles.
        # --------------------------
        for metric_id, values in metrics.items():
            metrics[metric_id]["percentiles"] = {"categories": dict()}
            if values["score"] is not None:
                for category_id in categories.keys():
                    metrics_records = MetricPercentile.query \
                        .join(CorpusMetricScore, CorpusMetricScore.id == MetricPercentile.corpus_metric_score_id) \
                        .add_columns(MetricPercentile.percentile) \
                        .filter(MetricPercentile.metric_id == metric_id) \
                        .filter(MetricPercentile.category_id == category_id) \
                        .filter(CorpusMetricScore.score <= metrics[metric_id]["score"]) \
                        .order_by(CorpusMetricScore.score.desc()) \
                        .first()

                    if metrics_records:
                        metrics[metric_id]["percentiles"]["categories"][category_id] = metrics_records.percentile
                    else:
                        metrics[metric_id]["percentiles"]["categories"][category_id] = 0.0

        return metrics, 200
