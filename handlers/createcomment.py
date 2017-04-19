from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.comment import Comment


class CreateComment(BlogHandler):

    """If user isn't signed in return user to the login page, otherwise render
    the create-comment.html template. """
    def get(self, post_id, user_id):
        if not self.user:
            self.render('/login')
        else:
            self.render("create-comment.html", post_id=post_id)

    """If user isn't signed in return user to the login page, otherwise create
    the comment in the db and redirect to the post page. """
    def post(self, post_id, user_id):
        if not self.user:
            return self.redirect('/login')

        content = self.request.get('content')
        user_name = self.user.name
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)
        c = Comment(parent=postkey, user=self.user.key(),
                    content=content, post=postkey)

        post.comment_count += 1

        c.put()
        post.put()

        self.redirect('/' + post_id)
