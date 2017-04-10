from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *

class EditPost(BlogHandler):
	def get(self, post_id, post_user_id):
		if self.user and self.user.key().id() == int(post_user_id):
			postKey = db.Key.from_path('Post', int(post_id), parent=blog_key())
			post = db.get(postkey)

			self.render("editpost.html", subject = post.subject, content=post.content, post_id = post_id)

		elif not self.user:
			self.redirect("/login")

		else:
			self.write("You do not have permission to edit this post")

	def post(self, post_id):
		if self.user and self.user.key().id() == int(post_user_id):
			postcontent = self.request.get('content')
			postsubject = self.request.get('subject')
			if postcontent and postsubject:
				postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
				post = db.get(postkey)
				post.content = postcontent
				post.subject = postsubject

				post.put()

				self.redirect('/%s' % str(post.key().id()))

			else:
				error_msg = "You do not have permission to edit this post"
				self.render("newpost.html", subject=subject,
							content=content, error=error_msg)

		elif not self.user:
			self.redirect("/login")

		else:
			self.write("You do not have permission to edit this post")

