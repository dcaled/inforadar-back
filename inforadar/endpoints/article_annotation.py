import random
import inforadar.config as config
from cerberus import Validator
from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.login.user import csrf_protection
from inforadar.models import ArticleAnnotationReply, MainArticleAnnotationReply
from ..constants import article_collections, article_collection_to_reply, annotation_reply


class ArticleAnnotation(Resource):

    @login_required
    def get(self):
        user_collection_ids = article_collections[current_user.collection]

        user_annotation_reply = article_collection_to_reply[current_user.collection]

        replyClass = ArticleAnnotationReply if user_annotation_reply == annotation_reply[
            "MINT"] else MainArticleAnnotationReply

        annotated_articles = replyClass.query \
            .filter(replyClass.user_id == current_user.id) \
            .with_entities(replyClass.corpus_article_id).all()

        annotated_articles_ids = set()
        # Add the ids of articles already annotated to a set.
        for article in annotated_articles:
            annotated_articles_ids.add(article.corpus_article_id)

        # Create a set containing the ids of articles that were not annotated.
        non_annotated_article_ids = user_collection_ids.difference(
            annotated_articles_ids)

        if len(non_annotated_article_ids) == 0:
            return 0

        selected_article_id = random.choice(tuple(non_annotated_article_ids))

        return selected_article_id

    @login_required
    @csrf_protection
    def post(self):
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        allowed_schema_mint = {
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

        allowed_schema_main = {
            "corpus_article_id": {"type": "integer", "required": True},
            "category": {"type": "integer", "required": True},
            "category_other": {"type": "string"},
            "credibility": {"type": "integer", "required": True},
            "representativeness": {"type": "integer", "required": True},
            "sensationalism": {"type": "integer", "required": True},
            "consistency": {"type": "integer", "required": True},
            "cites_sources": {"type": "integer", "required": True},
            # ifcite_sources
            "source_credibility": {"type": "integer"},
            "time_space": {"type": "integer", "required": True},
            "objectivity": {"type": "integer", "required": True},
            "fact_opinion": {"type": "integer", "required": True},
            # iffacts
            "accuracy": {"type": "integer"},
            # ifopinions
            "clear_viewpoint": {"type": "integer"},
            # ifopinions
            "author_conviction": {"type": "integer"},
            # ifopinions
            "unique_perspective": {"type": "integer"},
            # ifopinions
            "personal_perspective": {"type": "integer"},
            # ifopinions
            "clarity": {"type": "integer"},
            "appeal_to_fear": {"type": "integer", "required": True},
            "appeal_to_action": {"type": "integer", "required": True},
            "personal_attack": {"type": "integer", "required": True},
            "sarcasm": {"type": "integer", "required": True},
            "secret_society": {"type": "integer", "required": True},
            "evil_forces": {"type": "integer", "required": True},
            "threatening_truths": {"type": "integer", "required": True},
            "us_vs_them": {"type": "integer", "required": True},
            "conspiracy_themes": {"type": "list", "required": True},
            "conspiracy_themes_other": {"type": "string"},
            "sentiment_polarity": {"type": "integer", "required": True},
            "sentiment_intensity": {"type": "integer", "required": True},
            "emotion": {"type": "list", "required": True},
            "main_emotion": {"type": "integer", "required": True},
            "time_taken": {"type": "integer", "required": True},
        }

        user_annotation_reply = article_collection_to_reply[current_user.collection]

        allowed_schema = allowed_schema_mint if user_annotation_reply == annotation_reply[
            "MINT"] else allowed_schema_main

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
        ) if user_annotation_reply == annotation_reply["MINT"] \
            else MainArticleAnnotationReply(
            user_id=current_user.id,
            corpus_article_id=data["corpus_article_id"],
            category=data["category"],
            category_other=data.get("category_other", None),
            credibility=data["credibility"],
            representativeness=data["representativeness"],
            sensationalism=data["sensationalism"],
            consistency=data["consistency"],
            cites_sources=data["cites_sources"],
            source_credibility=data.get("source_credibility", None),
            time_space=data["time_space"],
            objectivity=data["objectivity"],
            fact_opinion=data["fact_opinion"],
            accuracy=data.get("accuracy", None),
            clear_viewpoint=data.get("clear_viewpoint", None),
            author_conviction=data.get("author_conviction", None),
            unique_perspective=data.get("unique_perspective", None),
            personal_perspective=data.get("personal_perspective", None),
            clarity=data.get("clarity", None),
            appeal_to_fear=data["appeal_to_fear"],
            appeal_to_action=data["appeal_to_action"],
            personal_attack=data["personal_attack"],
            sarcasm=data["sarcasm"],
            secret_society=data["secret_society"],
            evil_forces=data["evil_forces"],
            threatening_truths=data["threatening_truths"],
            us_vs_them=data["us_vs_them"],
            conspiracy_themes=data["conspiracy_themes"],
            conspiracy_themes_other=data.get("conspiracy_themes_other", None),
            sentiment_polarity=data["sentiment_polarity"],
            sentiment_intensity=data["sentiment_intensity"],
            emotion=data["emotion"],
            main_emotion=data["main_emotion"],
            time_taken=data["time_taken"],
        )

        config.db.session.add(article_annotation_reply)
        config.db.session.commit()

        return "", 204
