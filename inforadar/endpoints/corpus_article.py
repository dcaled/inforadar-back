from cerberus import Validator
from flask import request
from flask_login import login_required
from flask_restful import Resource
from inforadar.models import CorpusArticle, CorpusArticleSchema


class CorpusArticleInfo(Resource):

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

        corpus_article = CorpusArticle.query.get(request.args["id"])

        # Serialize the data for the response
        corpus_article_schema = CorpusArticleSchema()
        corpus_article_data = corpus_article_schema.dump(corpus_article)

        return corpus_article_data, 200
