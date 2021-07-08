import random

from cerberus import Validator
from flask import request
from flask_restful import Resource

import inforadar.config as config
from inforadar.models import Category, Metric, CorpusMetricQuartile, CrowdsourcedArticle, \
    CrowdsourcedMetricScore, MetricPercentile, CorpusMetricScore


class Metrics(Resource):
    def get(self):
        """
        Output: dictionary listing each metric, the corresponding description, and the quartiles for each category
        (fact, opinion, conspiracy, entertainment, and satire).
        """

        records = CorpusMetricQuartile.query \
            .join(Metric, Metric.id == CorpusMetricQuartile.metric_id) \
            .join(Category, Category.id == CorpusMetricQuartile.category_id) \
            .add_columns(Metric.id.label("metric_id"), Metric.name.label("metric_name"),
                         Metric.display_name, Metric.description,
                         Category.id.label("category_id"), Category.name.label("category_name"), Category.display_name,
                         CorpusMetricQuartile.first_quartile, CorpusMetricQuartile.second_quartile,
                         CorpusMetricQuartile.third_quartile).all()

        metrics = dict()
        for record in records:
            if record.metric_id not in metrics:
                metrics[record.metric_id] = {
                    "id": record.metric_id,
                    "name": record.metric_name,
                    "display_name": record.display_name,
                    "description": record.description,
                    "categories": []
                }
            metrics[record.metric_id]["categories"] += [{
                "id": record.category_id,
                "name": record.category_name,
                "display_name": record.display_name,
                "first_quartile": record.first_quartile,
                "second_quartile": record.second_quartile,
                "third_quartile": record.third_quartile
            }
            ]

        metrics = list(metrics.values())
        return metrics, 200

    def post(self):
        """
        Input: headline (optional ?), and body text (mandatory), list with metrics.
        Output: a dictionary listing the score and percentile for each category and each metric.
        """

        categories_records = Category.query.with_entities(Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        metrics_records = Category.query.with_entities(Metric.id, Metric.name).all()
        available_metrics = {record.id: record.name for record in metrics_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

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
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)
        metrics = dict()
        article_id = None

        # --------------------------
        # Persist article and retrieve existing metrics.
        # --------------------------
        if data.get("id", None):
            # metrics_records = Category.query.with_entities(Metric.id, Metric.name).all()
            article = CrowdsourcedArticle.query.filter_by(id=data["id"]).first()

            metrics_records = CrowdsourcedArticle.query \
                .join(CrowdsourcedMetricScore,
                      CrowdsourcedMetricScore.crowdsourced_article_id == CrowdsourcedArticle.id) \
                .add_columns(CrowdsourcedMetricScore.metric_id, CrowdsourcedMetricScore.score) \
                .filter(CrowdsourcedArticle.id == article.id) \
                .filter(CrowdsourcedMetricScore.metric_id.in_(data["metrics"])).all()

            for record in metrics_records:
                metrics[record.metric_id] = {"score": record.score}
            article_id = article.id

        # --------------------------
        # Compute score for each metric.
        # --------------------------
        new_metrics = dict()
        for metric_id in data.get("metrics"):
            if metric_id not in metrics.keys():
                # TODO:
                # metric_instance = instantiate_metric(metric)
                # score = metric_instance.compute_score(article)
                score = random.uniform(0, 1)
                new_metrics[metric_id] = {"score": score}
        metrics.update(new_metrics)

        # --------------------------
        # Persist new metrics.
        # --------------------------
        if article_id:
            for metric_id in new_metrics.keys():
                metric_score = CrowdsourcedMetricScore(metric_id=metric_id,
                                                       crowdsourced_article_id=article_id,
                                                       score=new_metrics[metric_id]["score"])
                config.db.session.add(metric_score)
            config.db.session.commit()

        # --------------------------
        # Get percentiles.
        # --------------------------
        a = []
        for metric_id in metrics.keys():
            metrics[metric_id]["percentiles"] = {"categories": dict()}
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
