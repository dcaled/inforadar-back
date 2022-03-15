import inforadar.config as config
from cerberus import Validator
from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource
from inforadar.login.user import csrf_protection
from inforadar.models import SocioDemographicReply


class SocioDemographic(Resource):

    @login_required
    def get(self):
        return True if SocioDemographicReply.query.filter_by(user_id=current_user.id).first() else False

    @login_required
    @csrf_protection
    def post(self):
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        allowed_schema = {
            "age": {"type": "integer", "required": True},
            "cs_qualifications": {"type": "integer", "required": True},
            "job": {"type": "integer", "required": True},
            "nationality": {"type": "integer", "required": True},
            "qualifications": {"type": "integer", "required": True},
            "consumed_content": {"type": "list", "required": True},
            "news_consumption": {"type": "integer", "required": True},
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        if self.get():
            return {"message": "Another reply already submitted."}, 400

        data = request.get_json(force=True)

        sociodemographic_reply = SocioDemographicReply(
            user_id=current_user.id,
            age=data["age"],
            cs_qualifications=data["cs_qualifications"],
            job=data["job"],
            nationality=data["nationality"],
            qualifications=data["qualifications"],
            consumed_content=str(data["consumed_content"]),
            news_consumption=data["news_consumption"]
        )

        config.db.session.add(sociodemographic_reply)
        config.db.session.commit()

        return "", 204
