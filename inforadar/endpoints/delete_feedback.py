from cerberus import Validator
from flask import request
from flask_restful import Resource

import inforadar.config as config
from inforadar.models import UserFeedback


class DeleteFeedback(Resource):
    def post(self):
        """
        Input: feedback id and feedback auth.
        """

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {
            "id": {"type": "integer", "required": True},
            "auth": {"type": "string",
                     "required": True,
                     },
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), schema)
        if not valid:
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # --------------------------
        # Retrieve existing indicators.
        # --------------------------

        feedback = UserFeedback.query.filter_by(
            id=data["id"]).first()
        if not feedback:
            return {'message': f"Invalid feedback id: {str(data['id'])}."}, 400

        if feedback.auth != data["auth"]:
            return {'message': f"Wrong authentication. You cannot delete this."}, 400

        # --------------------------
        # Persist new feedback.
        # --------------------------

        config.db.session.delete(feedback)
        config.db.session.commit()

        return "ok", 200
