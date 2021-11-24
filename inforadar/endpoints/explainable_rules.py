import json
from flask_restful import Resource

from ..constants import fp_explainable_rules


class ExplainableRules(Resource):
    def get(self):
        f = open(fp_explainable_rules)
        response = json.load(f)
        return response
