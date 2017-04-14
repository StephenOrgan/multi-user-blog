from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.like import Like

class Post(BlogHandler):
	def get(self, post_id):
		postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
		post = db.get(postkey)
		user_id = self.user.key().id()
		comments = db.GqlQuery(
			"select * from Comment where post_id = :1 order by created desc limit 10", postkey)
		likedpost = db.GqlQuery(
            "select * from Like where ancestor is :1 and user_id = :2", postkey, user_id)
		liked = likedpost.get()



		if not post:
			self.error(404)
			return

		self.render("permalink.html", post = post, comments = comments, liked = liked)