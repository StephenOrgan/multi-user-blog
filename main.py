# General
import webapp2
from webapp2 import WSGIApplication
from google.appengine.ext import db
from validate import *


# Models
from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like


# Handlers
from handlers.bloghandler import BlogHandler
from handlers.front import BlogFront
from handlers.signup import Signup

from handlers.welcome import Unit3Welcome
from handlers.mainpage import MainPage
from handlers.login import Login
from handlers.logout import Logout
from handlers.createcomment import CreateComment
from handlers.editcomment import EditComment
from handlers.deletecomment import DeleteComment

from handlers.post import Post
from handlers.newpost import NewPost
from handlers.deletepost import DeletePost
from handlers.editpost import EditPost

from handlers.like import LikeHandler
from handlers.like import UnlikeHandler



##### blog stuff

# this returns the key from the blog post.  The name allows us to have multiple blogs where default is the main schema?





app = webapp2.WSGIApplication([
								('/', BlogFront),
								('/signup', Signup),
								('/welcome', Unit3Welcome),
								('/?', BlogFront),
								('/login', Login),
								('/logout', Logout),
								('/([0-9]+)', Post),
								('/newpost', NewPost),
								('/([0-9]+)/editpost', EditPost),
								('/([0-9]+)/deletepost/([0-9]+)', DeletePost),
								('/([0-9]+)/addcomment/([0-9]+)', CreateComment),
								('/([0-9]+)/([0-9]+)/editcomment/([0-9]+)', EditComment),
								('/([0-9]+)/([0-9]+)/deletecomment/([0-9]+)', DeleteComment),
								('/([0-9]+)/like', LikeHandler),
								('/([0-9]+)/unlike', UnlikeHandler),
                               ],
                              debug=True)