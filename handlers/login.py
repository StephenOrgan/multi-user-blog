from handlers.bloghandler import BlogHandler
from models.user import User
from validate import *


class Login(BlogHandler):


    def get(self):
        """ Render the Login-Form """
        self.render('login-form.html')

    
    def post(self):
        """ If valid email and password login the user and redirect
        to the homepage"""
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            return self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
