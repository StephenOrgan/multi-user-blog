from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *


class DeleteComment(BlogHandler):

    
    def get(self, post_id, post_user_id, comment_id):
        """ If the user is signed in and the author of the post, deincrement
        the comment count in the post model and delete the comment from the
        db. Otherwise the user does not have permission to delete the comment. """
        if self.user and self.user.key().id() == int(post_user_id):
            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(postkey)
            commentkey = db.Key.from_path('Comment', int(comment_id),
                                          parent=postkey)
            comment = db.get(commentkey)

            post.comment_count -= 1

            comment.delete()
            post.put()

            return self.redirect('/' + str(postkey.id()))

        elif not self.user:
            return self.redirect("/login")

        else:
            error_msg = "You do not have permission to delete this comment"

            self.write(error_msg)
