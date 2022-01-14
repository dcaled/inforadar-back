import sys

from cerberus import Validator
from flask import request
from flask_restful import Resource

from sqlalchemy.sql.expression import func
import inforadar.config as config
from inforadar.models import Category, Metric, CorpusMetricScore, CorpusArticle


class Histogram(Resource):
    def post(self):
        metrics_records = Metric.query.with_entities(Metric.id, Metric.name).all()
        available_metrics = {record.id: record.name for record in metrics_records}

        categories_records = Category.query.with_entities(Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        allowed_schema = {
            "metrics": {"type": "list",
                        "required": True,
                        "allowed": available_metrics,
                        "schema": {"type": "integer"}
                        },
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        # --------------------------
        # Compute bins for each metric.
        # --------------------------
        data = request.get_json(force=True)
        metric_bins = dict()
        for metric_id in data.get("metrics"):
            metric_bins[metric_id] = {"categories": dict()}
            for category_id in categories.keys():
                # Create the list of bins from our data
                bins = config.db.session \
                    .query((func.floor(CorpusMetricScore.score / 0.001) * 0.001).label("floor"),
                           func.count(CorpusMetricScore.id).label("count")) \
                    .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .filter(CorpusArticle.category_id == category_id) \
                    .group_by("floor") \
                    .order_by("floor").all()

                # select
                #   floor(actions_count/100.00)*100 as bin_floor,
                #   count(user_id) as count
                # from product_actions
                # group by bin_floor
                # order by bin_floor;

                metric_bin = []
                for b in bins:
                    metric_bin.append({
                        "count": b.count,
                        "value": b.floor
                    })
                metric_bins[metric_id]["categories"][category_id] = metric_bin

        return metric_bins, 200
