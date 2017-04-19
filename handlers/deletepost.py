from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *


class DeletePost(BlogHandler):

    
    def get(self, post_id, post_user_id):
        """ If the user is signed in and authored the post, delete the post and
        redirect the user to the homepage.  Otherwise, send non-signed in users
        to the login page. For all other cases go back to the current page with
        a permission error. """
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
            "select * from Comment where ancestor is :1 order by created desc limit 10", postkey) # NOQA

            self.render("permalink.html", post=post, comments=comments,
                        error_msg=error_msg)
