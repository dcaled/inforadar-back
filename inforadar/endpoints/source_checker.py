from cerberus import Validator
from flask import request
from flask_restful import Resource

from inforadar.models import ErcSource

import tldextract


class SourceChecker(Resource):
    def post(self):
        """
        Receives an url, and checks if the source is validated by ERC.
        Input: news article's url.
        Output: ERC registration number if the source is registered, and None otherwise.
        """

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {'url': {'type': 'string', 'required': True}, }

        validator = Validator(schema)
        validator.validate(request.get_json(force=True))
        if not validator.validate(request.get_json(force=True)):
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # Check if URL subdomain (or domain) belongs to a verified source.
        ext = tldextract.extract(data["url"])
        domain = "{}.{}".format(ext.domain, ext.suffix)
        subdomain = "{}.{}.{}".format(ext.subdomain, ext.domain, ext.suffix).replace("www.", "")

        erc_source_subdomain = ErcSource.query.filter_by(domain=subdomain).first()
        erc_source_domain = ErcSource.query.filter_by(domain=domain).first()

        if erc_source_subdomain:
            # print(erc_source_subdomain.title, erc_source_subdomain.registration_number)
            return erc_source_subdomain.registration_number, 200
        elif erc_source_domain:
            # print(erc_source_domain.title, erc_source_domain.registration_number)
            return erc_source_domain.registration_number, 200
        # Subdomain and domain not found.
        else:
            return None, 200

