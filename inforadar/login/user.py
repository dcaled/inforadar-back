from flask import request
from flask_login import UserMixin

import inforadar.config as config
from inforadar.models import User


class UserClass(UserMixin):
    """ User class that stores ID and name and others """

    def __init__(self, ident, google_id, name, email, annotator, collection, admin, created_at):
        self.id = ident
        self.google_id = google_id
        self.name = name
        self.email = email
        self.annotator = annotator
        self.collection = collection
        self.admin = admin
        self.created_at = created_at


# A user manager.
class UserManager():

    def get_google_user(google_subscriber_id):
        """Get user profile info."""

        user = User.query.filter_by(google_id=google_subscriber_id).first()
        return UserManager.userclass_from_usermodel(user) if user else None

    def add_google_user(google_subscriber_id, name, email, annotator, collection):
        """Add user profile info."""

        user = User(google_id=google_subscriber_id,
                    name=name, email=email, annotator=annotator, collection=collection, admin=False)
        config.db.session.add(user)
        config.db.session.commit()
        return UserManager.userclass_from_usermodel(user)

    def lookup_user(user_id):
        """Lookup user by ID. Returns User object."""
        user = User.query.get(user_id)
        return UserManager.userclass_from_usermodel(user) if user else None

    def userclass_from_usermodel(usermodel):
        return UserClass(usermodel.id, usermodel.google_id, usermodel.name, usermodel.email, usermodel.annotator, usermodel.collection, usermodel.admin, usermodel.created_at)


# Decorator to add CSRF protection to any mutating function.
#
# Adding this header to the client forces the browser to first do an OPTIONS
# call, determine that the origin is not allowed, and block the subsequent
# call. (Ordinarily, the call is made but the result not made available to
# the client if the origin is not allowed, but the damage is already done.)
# Checking for the presence of this header on the server side prevents
# clients from bypassing this check.
#
# Add this decorator to all mutating operations.
def csrf_protection(fn):
    """Require that the X-Requested-With header is present."""
    def protected(*args):
        if 'X-Requested-With' in request.headers:
            return fn(*args)
        else:
            return "X-Requested-With header missing", 403
    return protected


# The user loader looks up a user by their user ID, and is called by
# flask-login to get the current user from the session. Return None
# if the user ID isn't valid.


@config.login.user_loader
def user_loader(user_id):
    return UserManager.lookup_user(user_id)
