from flask import request
from flask_login import UserMixin


class User(UserMixin):
    """Simple User class that stores ID, name, and profile image."""

    def __init__(self, ident, name, profile_pic):
        self.id = ident
        self.name = name
        self.profile_pic = profile_pic

    def update(self, name, profile_pic):
        self.name = name
        self.profile_pic = profile_pic


# A simple user manager.  A real world application would implement the same
# interface but using a database as a backing store.  Note that this
# implementation will behave unexpectedly if the user contacts multiple
# instances of the application since it is using an in-memory store.
class UserManager(object):
    """Simple user manager class.

    Replace with something that talks to your database instead.
    """

    def __init__(self):
        self.known_users = {}

    def add_or_update_google_user(self, google_subscriber_id, name,
                                  profile_pic):
        """Add or update user profile info."""
        if google_subscriber_id in self.known_users:
            self.known_users[google_subscriber_id].update(name, profile_pic)
        else:
            self.known_users[google_subscriber_id] = \
                User(google_subscriber_id, name, profile_pic)
        return self.known_users[google_subscriber_id]

    def lookup_user(self, google_subscriber_id):
        """Lookup user by ID.  Returns User object."""
        return self.known_users.get(google_subscriber_id)


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
