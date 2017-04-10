from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *

class EditComment(BlogHandler):
	def get(self, post_id, post_user_id, comment_id):
		if self.user and self.user.key().id() == int(post_user_id):
			postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			commentkey = db.Key.from_path('Comment', int(comment_id), parent=postKey)
			comment = db.get(postkey)

			self.render("editcomment.html", content=comment.content)

		elif not self.user:
			self.redirect("/login")

		else:
			self.write("You do not have permission to edit this comment")

	def post(self, post_id, post_user_id, comment_id):
		if self.user and self.user.key().id() == int(post_user_id):
			formcontent = self.request.get('content')
			postKey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			commentkey = db.Key.from_path('Comment', int(comment_id), parent=postKey)
			comment = db.get(key)
			comment.content = formcontent
			comment.put()

			self.redirect('/' + post_id)

		elif not self.user:
			self.redirect("/login")

		else:
			self.write("You do not have permission to edit this comment")



