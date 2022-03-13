from cerberus import Validator
from flask import request
from flask_restful import Resource

import inforadar.config as config
from inforadar.classify.classify import classify_text
from inforadar.models import Category, Indicator, CrowdsourcedArticle, CrowdsourcedIndicatorScore, IndicatorSchema
from ..constants import current_version_indicator_1


class Indicators(Resource):
    def get(self):
        """
        Output: dictionary listing each indicator, the corresponding description, and the quartiles for each category
        (fact, opinion, conspiracy, entertainment, and satire).
        """

        # Create the list of indicators from our data.
        indicator = Indicator.query.all()

        # Serialize the data for the response
        indicator_schema = IndicatorSchema(many=True)
        indicator_data = indicator_schema.dump(indicator)

        return indicator_data, 200

    def post(self):
        """
        Input: headline (optional ?), and body text (mandatory), list with indicators.
        Output: a dictionary listing the score and percentile for each category and each indicator.
        """

        categories_records = Category.query.with_entities(Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        indicators_records = Indicator.query.with_entities(Indicator.id, Indicator.name).all()
        available_indicators = {record.id: record.name for record in indicators_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema_1 = {
            "id": {"type": "integer", "required": True},
            "indicators": {"type": "list",
                           "required": True,
                           "allowed": available_indicators,
                           "schema": {"type": "integer"}
                           },
        }

        schema_2 = {
            "headline": {"type": "string", "required": True},
            "body_text": {"type": "string", "required": True},
            "indicators": {"type": "list", "required": True,
                           "allowed": available_indicators,
                           "schema": {"type": "integer"}
                           },
        }

        validator = Validator()
        valid = any(validator(request.get_json(force=True), schema) for schema in [schema_1, schema_2])
        if not valid:
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)
        indicators = dict()
        article_id = None

        # --------------------------
        # Persist article and retrieve existing indicators.
        # --------------------------
        if data.get("id", None):
            # indicators_records = Category.query.with_entities(Metric.id, Metric.name).all()
            article = CrowdsourcedArticle.query.filter_by(id=data["id"]).first()
            if not article:
                return {'message': f"Invalid article id: " + str(data["id"]) + "."}, 400
            article_id = article.id
            body_text = article.body_text

            # TODO: Attention: when a new version of the indicators calculator is released, you should update this
            #  query to retrieve the score of the current indicator calculator.
            indicators_records = CrowdsourcedArticle.query \
                .join(CrowdsourcedIndicatorScore,
                      CrowdsourcedIndicatorScore.crowdsourced_article_id == CrowdsourcedArticle.id) \
                .add_columns(CrowdsourcedIndicatorScore.indicator_id,
                             CrowdsourcedIndicatorScore.category_id,
                             CrowdsourcedIndicatorScore.score) \
                .filter(CrowdsourcedArticle.id == article.id) \
                .filter(CrowdsourcedIndicatorScore.indicator_id.in_(data["indicators"])).all()

            for record in indicators_records:
                if record.indicator_id in indicators:
                    indicators[record.indicator_id]['categories'][record.category_id] = {"score": record.score}
                else:
                    indicators[record.indicator_id] = {'categories': {record.category_id: {"score": record.score}}}
        else:
            body_text = data.get("body_text", None)

        # --------------------------
        # Compute score for each indicator.
        # --------------------------
        new_indicators = dict()
        for indicator_id in data.get("indicators"):
            if indicator_id not in indicators.keys():
                scores = classify_text(body_text)
                new_indicators[indicator_id] = scores
        indicators.update(new_indicators)

        # --------------------------
        # Persist new indicators.
        # --------------------------
        if article_id:
            for indicator_id in new_indicators.keys():
                for category_id in categories:
                    indicator_score = CrowdsourcedIndicatorScore(
                        indicator_id=indicator_id,
                        category_id=category_id,
                        crowdsourced_article_id=article_id,
                        score=new_indicators[indicator_id]['categories'][category_id]["score"],
                        version=current_version_indicator_1
                    )
                    config.db.session.add(indicator_score)
            config.db.session.commit()

        return indicators, 200
