from sqlalchemy.sql import func
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.models import ArticleAnnotationReply, MainArticleAnnotationReply, User
from ..constants import article_collections_strings, article_collection_to_reply, annotation_reply


class UserReports(Resource):

    @login_required
    def get(self):

        if (not current_user.admin):
            return {'message': "Only accessible to admins."}, 403

        users = User.query.order_by(User.id)

        result = []

        for user in users:

            user_annotation_reply = article_collection_to_reply[user.collection]

            replyClass = ArticleAnnotationReply \
                if user_annotation_reply == annotation_reply["MINT"] else MainArticleAnnotationReply

            articles = replyClass.query \
                .filter(replyClass.user_id == user.id) \
                .with_entities(func.avg(replyClass.time_taken).label('avg_time_taken'), func.count().label('sum_articles')).first()

            result.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'annotator': user.annotator,
                'articles': str(articles.sum_articles),
                'avg_time_taken': str(articles.avg_time_taken),
                'collection': article_collections_strings[user.collection],
            })

        return result, 200
