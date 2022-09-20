import random
import inforadar.config as config
from cerberus import Validator
from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.login.user import csrf_protection
from inforadar.models import ArticleAnnotationReply
from ..constants import article_collections


class ArticleAnnotation(Resource):

    @login_required
    def get(self):
        user_collection_ids = article_collections[current_user.collection]

        annotated_articles = ArticleAnnotationReply.query \
            .filter(ArticleAnnotationReply.user_id == current_user.id) \
            .with_entities(ArticleAnnotationReply.corpus_article_id).all()

        annotated_articles_ids = set()
        # Add the ids of articles already annotated to a set.
        for article in annotated_articles:
            annotated_articles_ids.add(article.corpus_article_id)

        # Create a set containing the ids of articles that were not annotated.
        non_annotated_article_ids = user_collection_ids.difference(
            annotated_articles_ids)
        selected_article_id = random.choice(tuple(non_annotated_article_ids))

        return selected_article_id

    @login_required
    @csrf_protection
    def post(self):
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        allowed_schema = {
            "corpus_article_id": {"type": "integer", "required": True},
            "likely_being_factual": {"type": "integer", "required": True},
            "likely_being_opinion": {"type": "integer", "required": True},
            "likely_being_entertainment": {"type": "integer", "required": True},
            "likely_being_satire": {"type": "integer", "required": True},
            "likely_being_conspiracy": {"type": "integer", "required": True},
            "pre_credibility": {"type": "integer", "required": True},
            "change_in_perception": {"type": "integer", "required": True},
            "info_is_useful": {"type": "integer", "required": True},
            "info_reflected_in_subjectivity": {"type": "integer", "required": True},
            "relevance_of_subjectivity": {"type": "integer", "required": True},
            "info_reflected_in_spell_checking": {"type": "integer", "required": True},
            "relevance_of_spell_checking": {"type": "integer", "required": True},
            "info_reflected_in_sentiment": {"type": "integer", "required": True},
            "relevance_of_sentiment": {"type": "integer", "required": True},
            "info_reflected_in_headline_accuracy": {"type": "integer", "required": True},
            "relevance_of_headline_accuracy": {"type": "integer", "required": True},
            "info_reflected_in_clickbait": {"type": "integer", "required": True},
            "relevance_of_clickbait": {"type": "integer", "required": True},
            "most_relevant_metric": {"type": "integer", "required": True},
            "least_relevant_metric": {"type": "integer", "required": True},
            "time_taken":  {"type": "integer", "required": True},
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        article_annotation_reply = ArticleAnnotationReply(
            user_id=current_user.id,
            corpus_article_id=data["corpus_article_id"],
            likely_being_factual=data["likely_being_factual"],
            likely_being_opinion=data["likely_being_opinion"],
            likely_being_entertainment=data["likely_being_entertainment"],
            likely_being_satire=data["likely_being_satire"],
            likely_being_conspiracy=data["likely_being_conspiracy"],
            pre_credibility=data["pre_credibility"],
            change_in_perception=data["change_in_perception"],
            info_is_useful=data["info_is_useful"],
            info_reflected_in_subjectivity=data["info_reflected_in_subjectivity"],
            relevance_of_subjectivity=data["relevance_of_subjectivity"],
            info_reflected_in_spell_checking=data["info_reflected_in_spell_checking"],
            relevance_of_spell_checking=data["relevance_of_spell_checking"],
            info_reflected_in_sentiment=data["info_reflected_in_sentiment"],
            relevance_of_sentiment=data["relevance_of_sentiment"],
            info_reflected_in_headline_accuracy=data["info_reflected_in_headline_accuracy"],
            relevance_of_headline_accuracy=data["relevance_of_headline_accuracy"],
            info_reflected_in_clickbait=data["info_reflected_in_clickbait"],
            relevance_of_clickbait=data["relevance_of_clickbait"],
            most_relevant_metric=data["most_relevant_metric"],
            least_relevant_metric=data["least_relevant_metric"],
            time_taken=data["time_taken"],
        )

        config.db.session.add(article_annotation_reply)
        config.db.session.commit()

        return "", 204
