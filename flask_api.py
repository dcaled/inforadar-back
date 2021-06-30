from flask_restful import Api

from config import app

from endpoints.indicators import Indicators
from endpoints.metadata import Metadata
from endpoints.metrics import Metrics
from endpoints.scrapper import Scraper


api = Api(app)

api.add_resource(Indicators, '/indicators')
api.add_resource(Metrics, '/metrics')
api.add_resource(Scraper, '/scrapper')
api.add_resource(Metadata, '/metadata')

if __name__ == '__main__':
    app.run()
