from flask_restful import Api

from inforadar.config import app
from inforadar.endpoints.article_annotation import ArticleAnnotation
from inforadar.endpoints.corpus_article import CorpusArticleInfo
from inforadar.endpoints.crowdsourced_article import CrowdsourcedArticleInfo
from inforadar.endpoints.feedback import Feedback
from inforadar.endpoints.histogram import Histogram
from inforadar.endpoints.indicators import Indicators
from inforadar.endpoints.me import Me
from inforadar.endpoints.metadata import Metadata
from inforadar.endpoints.metrics import Metrics
from inforadar.endpoints.scrapper import Scraper
from inforadar.endpoints.sociodemographic import SocioDemographic
from inforadar.endpoints.source_checker import SourceChecker
from inforadar.endpoints.explainable_rules import ExplainableRules
from inforadar.endpoints.examples import Examples
from inforadar.endpoints.user_replies import UserReplies
from inforadar.endpoints.user_reports import UserReports

api = Api(app)

api.add_resource(Indicators, '/api2/indicators')
api.add_resource(Metrics, '/api2/metrics')
api.add_resource(Scraper, '/api2/scrapper')
api.add_resource(Metadata, '/api2/metadata')
api.add_resource(SourceChecker, '/api2/source_checker')
api.add_resource(ExplainableRules, '/api2/explainable_rules')
api.add_resource(Examples, '/api2/examples')
api.add_resource(Histogram, '/api2/histogram')
api.add_resource(Feedback, '/api2/feedback')
api.add_resource(Me, '/api2/me')
api.add_resource(SocioDemographic, '/api2/sociodemographic')
api.add_resource(ArticleAnnotation, '/api2/article_annotation')
api.add_resource(CorpusArticleInfo, '/api2/corpus_article')
api.add_resource(CrowdsourcedArticleInfo, '/api2/crowdsourced_article')
api.add_resource(UserReplies, '/api2/user_replies')
api.add_resource(UserReports, '/api2/user_reports')


if __name__ == '__main__':
    app.run()
