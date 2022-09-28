from sqlalchemy.sql import func
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.models import ArticleAnnotationReply, User


class UserReports(Resource):

    @login_required
    def get(self):

        if (not current_user.admin):
            return {'message': "Only accessible to admins."}, 403

        users = User.query.order_by(User.id).filter(User.annotator == True)

        result = []

        for user in users:

            articles = ArticleAnnotationReply.query \
                .filter(ArticleAnnotationReply.user_id == user.id) \
                .with_entities(func.avg(ArticleAnnotationReply.time_taken).label('avg_time_taken'), func.count().label('sum_articles')).first()

            result.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'articles': str(articles.sum_articles),
                'avg_time_taken': str(articles.avg_time_taken),
                'collection': user.collection,
            })

        return result, 200
