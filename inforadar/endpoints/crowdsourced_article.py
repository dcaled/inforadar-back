from cerberus import Validator
from flask import request
from flask_login import login_required
from flask_restful import Resource
from inforadar.models import CrowdsourcedArticle, CrowdsourcedArticleSchema


class CrowdsourcedArticleInfo(Resource):

    # @login_required
    def get(self):
        if not request.args:
            return {"message": f"Missing a JSON query in the request."}, 422

        allowed_schema = {
            "id": {"type": "string", "required": True},
        }

        validator = Validator()
        valid = validator(request.args, allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        crowdsourced_article = CrowdsourcedArticle.query.get(request.args["id"])

        # Serialize the data for the response
        crowdsourced_article_schema = CrowdsourcedArticleSchema()
        crowdsourced_article_data = crowdsourced_article_schema.dump(crowdsourced_article)

        return crowdsourced_article_data, 200
