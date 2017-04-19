from handlers.bloghandler import BlogHandler
from models.user import User
from validate import *


class Login(BlogHandler):

    """ Render the Login-Form """
    def get(self):
        self.render('login-form.html')

    """ If valid email and password login the user and redirect
    to the homepage"""
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
