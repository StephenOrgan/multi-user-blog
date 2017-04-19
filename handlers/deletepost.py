from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.like import Like
from models.comment import Comment


def delete_dependents(comments, likes):
        if comments:
            for c in comments:
                c.delete()
        if likes:
            for l in likes:
                l.delete()
                

class DeletePost(BlogHandler):

    
    def get(self, post_id, post_user_id):
        """ If the user is signed in and authored the post, delete the post and
        redirect the user to the homepage.  Otherwise, send non-signed in users
        to the login page. For all other cases go back to the current page with
        a permission error. """
        if self.user and self.user.key().id() == int(post_user_id):
            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(postkey)
            comments = Comment.all().filter('post =', postkey)
            likes = Like.all().filter('post_id =', post.key().id())

            if post:
                delete_dependents(comments=comments, likes=likes)
                post.delete()
                return self.redirect('/')

        elif not self.user:
            return self.redirect("/login")

        else:
            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(postkey)
            error_msg = "You do not have permission to delete this post"
            comments = db.GqlQuery(
            "select * from Comment where ancestor is :1 order by created desc limit 10", postkey) # NOQA

            self.render("permalink.html", post=post, comments=comments,
                        error_msg=error_msg)


