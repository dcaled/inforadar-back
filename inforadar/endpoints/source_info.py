from cerberus import Validator
from flask import request
from flask_restful import Resource

from inforadar.models import ErcSource, ErcSourceSchema


class SourceInfo(Resource):
    def post(self):
        """
        Receives an ERC registration number, and returns underlying data regarding the corresponding source.
        Input: ERC registration number.
        Output: Source data, according ERC registers. If the provided registration number is not found, returns None.
        """

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {'registration_number': {'type': 'integer', 'required': True}, }

        validator = Validator(schema)
        validator.validate(request.get_json(force=True))
        if not validator.validate(request.get_json(force=True)):
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # Filter by ERC registration number.
        erc_source = ErcSource.query.filter_by(registration_number=data["registration_number"]).first()
        if erc_source:
            # Serialize the data for the response
            erc_source_schema = ErcSourceSchema(many=False)
            erc_source_data = erc_source_schema.dump(erc_source)
            return erc_source_data, 200
        # No source found.
        else:
            return None, 200
