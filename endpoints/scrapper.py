from cerberus import Validator
from flask import request
from flask_restful import Resource

import config as config
from models import CrowdsourcedArticle


class Scraper(Resource):
    def post(self):
        """
        Receives an url, extracts the data, stores the data into the db, and returns the data.
        Input: url
        Output: parsed content
        """

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {'url': {'type': 'string', 'required': True},}

        validator = Validator(schema)
        validator.validate(request.get_json(force=True))
        if not validator.validate(request.get_json(force=True)):
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # --------------------------
        # Check if article is in database and, if not, insert it on database.
        # --------------------------
        article = CrowdsourcedArticle.query.filter_by(url=data["url"]).first()
        if not article:
            # TODO:
            headline = "Headline do artigo {}".format(data["url"])
            body_text = "Corpo do artigo {}.".format(data["url"])

            article = CrowdsourcedArticle(headline=headline, body_text=body_text, url=data["url"])
            config.db.session.add(article)
            config.db.session.commit()

        article = {
            "id": article.id,
            "url": article.url,
            "headline": article.headline,
            "body_text": article.body_text,
        }
        return article, 200

