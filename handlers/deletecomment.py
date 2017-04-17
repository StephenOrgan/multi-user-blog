from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *

class DeleteComment(BlogHandler):
	def get(self, post_id, post_user_id, comment_id):
		if self.user and self.user.key().id() == int(post_user_id):
			postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			commentkey = db.Key.from_path('Comment', int(comment_id), parent=postkey)
			comment = db.get(commentkey)
			
			comment.delete()

			self.redirect('/'+ str(postkey.id()))

		elif not self.user:
			self.redirect("/login")

		else:
			error_msg = "You do not have permission to delete this comment"
			
			self.write(error_msg)