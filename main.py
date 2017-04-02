# General
import webapp2
from webapp2 import WSGIApplication
from google.appengine.ext import db
from validate import *


# Models
from models.user import User
from models.post import Post



# Handlers
from handlers.bloghandler import BlogHandler
from handlers.front import BlogFront
from handlers.signup import Signup
from handlers.post import Post
from handlers.newpost import NewPost
from handlers.welcome import Unit3Welcome
from handlers.mainpage import MainPage





##### blog stuff

# this returns the key from the blog post.  The name allows us to have multiple blogs where default is the main schema?





app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', Signup),
                               ('/welcome', Unit3Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', Post),
                               ('/blog/newpost', NewPost),
                               ],
                              debug=True)