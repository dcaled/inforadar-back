from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from http import HTTPStatus
import inforadar.config as config
from inforadar.google_token import validate_id_token

from inforadar.login.user import UserManager, csrf_protection
from inforadar.models import SocioDemographicReply


class Me(Resource):
    """The currently logged-in user.

    GET will return information about the user if a session exists.
    POST will login a user given an ID token, and set a session cookie.
    DELETE will log out the currently logged-in user.
    """

    @login_required
    def get(self):
        return jsonify({
            'id': current_user.id,
            'google_id': current_user.google_id,
            'name': current_user.name,
            'annotator': current_user.annotator,
            'admin': current_user.admin,
            'sociodemographic': True if SocioDemographicReply.query.filter_by(user_id=current_user.id).first() else False,
        })

    @csrf_protection
    def post(self):
        # Validate the identity
        id_token = request.form.get('id_token')
        if id_token is None:
            return "No ID token provided", HTTPStatus.FORBIDDEN

        try:
            identity = validate_id_token(
                id_token, config.app.config['GOOGLE_CLIENT_ID'])
        except ValueError:
            return 'Invalid ID token', HTTPStatus.FORBIDDEN

        # Get the user info out of the validated identity
        if ('sub' not in identity or 'name' not in identity):
            return "Unexpected authorization response", HTTPStatus.FORBIDDEN

        # This just adds a new user that hasn't been seen before and assumes it
        # will work, but you could extend the logic to do something different
        # (such as only allow known users, or somehow mark a user as new so
        # your frontend can collect extra profile information).
        user = UserManager.add_or_get_google_user(
            identity['sub'], identity['name'])

        # Authorize the user:
        login_user(user, remember=True)

        return self.get()

    @login_required
    @csrf_protection
    def delete(self):
        logout_user()
        return "", HTTPStatus.NO_CONTENT
