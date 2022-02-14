import secrets
from cerberus import Validator
from flask import request
from flask_restful import Resource

import inforadar.config as config
from inforadar.models import Category, Indicator, CrowdsourcedArticle, CrowdsourcedIndicatorScore, UserFeedback


class Feedback(Resource):
    def post(self):
        """
        Input: article id and feedback indicators.
        Output: id of feedback saved in the database.
        """

        categories_records = Category.query.with_entities(
            Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        indicators_records = Indicator.query.with_entities(
            Indicator.id, Indicator.name).all()
        available_indicators = {
            record.id: record.name for record in indicators_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {
            "id": {"type": "integer", "required": True},
            "indicator": {"type": "integer",
                          "required": True,
                          "allowed": available_indicators,
                          },
            "main_category": {"type": "integer",
                              "required": True,
                              "allowed": categories,
                              },
            "suggested_category": {"type": "integer",
                                   "required": True,
                                   "allowed": categories,
                                   },
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), schema)
        if not valid:
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # --------------------------
        # Retrieve existing indicators.
        # --------------------------

        article = CrowdsourcedArticle.query.filter_by(
            id=data["id"]).first()
        if not article:
            return {'message': f"Invalid article id: {str(data['id'])}."}, 400
        article_id = article.id

        # TODO: Attention: when a new version of the indicators calculator is released, you should update this
        #  query to retrieve the score of the current indicator calculator.
        indicator_records = CrowdsourcedArticle.query \
            .join(CrowdsourcedIndicatorScore,
                  CrowdsourcedIndicatorScore.crowdsourced_article_id == CrowdsourcedArticle.id) \
            .add_columns(CrowdsourcedIndicatorScore.indicator_id,
                         CrowdsourcedIndicatorScore.category_id,
                         CrowdsourcedIndicatorScore.score,
                         CrowdsourcedIndicatorScore.version) \
            .filter(CrowdsourcedArticle.id == article.id) \
            .filter(CrowdsourcedIndicatorScore.indicator_id == data["indicator"]) \
            .order_by(CrowdsourcedIndicatorScore.score.desc()).all()

        if len(indicator_records) == 0:
            return {'message': f"Article not evaluated"}, 400

        main_category_indicator_record = indicator_records[0]

        if main_category_indicator_record.category_id != data["main_category"]:
            return {'message': f"Main category reported {str(data['main_category'])} not matching."}, 400

        # --------------------------
        # Persist new feedback.
        # --------------------------
        auth = secrets.token_hex(32)

        user_feedback = UserFeedback(
            user_id=0,
            crowdsourced_article_id=article_id,
            indicator_version=main_category_indicator_record.version,
            suggested_category=data["suggested_category"],
            main_category=main_category_indicator_record.category_id,
            indicator_id=main_category_indicator_record.indicator_id,
            auth=auth
        )
        config.db.session.add(user_feedback)
        config.db.session.commit()
        config.db.session.refresh(user_feedback)

        return {"id": user_feedback.id, "auth": auth}, 200
