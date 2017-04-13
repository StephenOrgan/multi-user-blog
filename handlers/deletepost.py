from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *

class DeletePost(BlogHandler):
	def get(self, post_id, post_user_id):
		if self.user and self.user.key().id() == int(post_user_id):
			postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			post = db.get(postkey)
			post.delete()
			self.redirect('/')

		elif not self.user:
			self.redirect("/login")

		else:
			postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			post = db.get(postkey)
			error_msg = "You do not have permission to delete this post"
			comments = db.GqlQuery(
				"select * from Comment where ancestor is :1 order by created desc limit 10", postkey)

			self.render("permalink.html", post = post, comments = comments, error_msg = error_msg)