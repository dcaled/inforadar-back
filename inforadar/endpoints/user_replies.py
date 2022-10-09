from cerberus import Validator
from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.models import ArticleAnnotationReply, User


class UserReplies(Resource):

    @login_required
    def get(self):

        if (not current_user.admin):
            return {"message": "Only accessible to admins."}, 403

        if not request.args:
            return {"message": "Missing a JSON query in the request."}, 422

        allowed_schema = {
            "id": {"type": "string", "required": True},
        }

        validator = Validator()
        valid = validator(request.args, allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: {str(validator.errors)}"}, 400

        if not User.query.filter(User.id == request.args["id"]).all():
            return {"message": "User with such ID not present."}, 400

        articles = ArticleAnnotationReply.query \
            .filter(ArticleAnnotationReply.user_id == request.args["id"]).all()

        result = []

        for article in articles:

            result.append({
                'article_id': article.corpus_article_id,
                'created_at': str(article.created_at),
                'time_taken': article.time_taken,
            })

        return result, 200
