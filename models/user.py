from google.appengine.ext import db
from validate import *


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, uid):
        """ load the user from the db by ID. """
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """ load user from db by filtering all users by that username """
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """ create an instance of the user. It does not store in the db """
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    
    @classmethod
    def login(cls, name, pw):
        """ Upon login check username and password """
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
