from flask_restful import Api

from inforadar.config import app
from inforadar.endpoints.indicators import Indicators
from inforadar.endpoints.metadata import Metadata
from inforadar.endpoints.metrics import Metrics
from inforadar.endpoints.scrapper import Scraper
from inforadar.endpoints.source_checker import SourceChecker
from inforadar.endpoints.explainable_rules import ExplainableRules

api = Api(app)

api.add_resource(Indicators, '/api2/indicators')
api.add_resource(Metrics, '/api2/metrics')
api.add_resource(Scraper, '/api2/scrapper')
api.add_resource(Metadata, '/api2/metadata')
api.add_resource(SourceChecker, '/api2/source_checker')
api.add_resource(ExplainableRules, '/api2/explainable_rules')


if __name__ == '__main__':
    app.run()
