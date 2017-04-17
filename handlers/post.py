from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.like import Like
from models.comment import Comment

class Post(BlogHandler):
	def get(self, post_id):
		postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
		post = db.get(postkey)
		comments = Comment.all().filter('post_id =', int(post_id))
		
		if self.user:
			user_id = self.user.key().id()
			likedpost = db.GqlQuery(
            	"select * from Like where ancestor is :1 and user_id = :2", postkey, user_id)
			liked = likedpost.get()
		else:
			liked = None



		if not post:
			self.error(404)
			return

		self.render("permalink.html", post = post, comments = comments, liked = liked)