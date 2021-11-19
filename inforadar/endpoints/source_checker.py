from cerberus import Validator
from flask import request
from flask_restful import Resource

from inforadar.models import ErcSource, ErcSourceSchema

import tldextract


class SourceChecker(Resource):
    def get(self):

        #TODO: This is a temporary solution. The field names should be in a custom config file in the front-end.

        fields = {
            "district": "Distrito",
            "registration_number": "Número de registo",
            "registration_date": "Data de inscrição",
            "title": "Título",
            "periodicity": "Periodicidade",
            "director": "Diretor",
            "owner": "Proprietário",
            "office_address": "Sede de redação",
            "location": "Localidade",
            "postal_code": "Código Postal",
            "municipality": "Concelho",
            "support": "Suporte",
            "institutional_email": "E-mail",
            "website": "Site",
            "content_type": "Conteúdo",
            "geographic_scope": "Âmbito geográfico",
            "editor": "Editor"
        }
        return fields

    def post(self):
        """
        Receives an url, and checks if the source is validated by ERC.
        Input: news article's url.
        Output: Source data, according ERC registers. If the provided registration number is not found, returns None.
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
            # Serialize the data for the response
            erc_source_schema = ErcSourceSchema(many=False)
            erc_source_data = erc_source_schema.dump(erc_source_subdomain)
            return erc_source_data, 200

        elif erc_source_domain:
            # print(erc_source_domain.title, erc_source_domain.registration_number)
            # Serialize the data for the response
            erc_source_schema = ErcSourceSchema(many=False)
            erc_source_data = erc_source_schema.dump(erc_source_domain)
            return erc_source_data, 200
        # Subdomain and domain not found.
        else:
            return None, 200


