from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *


class EditPost(BlogHandler):

    """ If the user is signed in and authored the post - render the
    edit-post.html template.  Users that are not signed in are redirected to
    the login page. Otherwise the user does not have permission to edit the
    post. """
    def get(self, post_id):
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)

        if self.user and self.user.key().id() == int(post.user_id):

            self.render("editpost.html", subject=post.subject,
                        content=post.content, post_id=post_id)

        elif not self.user:
            self.redirect("/login")

        else:
            self.write("You do not have permission to edit this post")

    """ If the user is signed in and authored the post - update the post in the
    db with the new content.  Users that are not signed in are redirected to
    the login page. Otherwise the user does not have permission to edit
    the post. """
    def post(self, post_id):
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)
        if self.user and self.user.key().id() == int(post.user_id):
            postcontent = self.request.get('content')
            postsubject = self.request.get('subject')

            if postcontent and postsubject:
                post.content = postcontent
                post.subject = postsubject

                post.put()

                self.redirect('/%s' % str(post.key().id()))

            else:
                error_msg = "You do not have permission to edit this post"
                self.render("editpost.html", subject=postsubject,
                            content=postcontent, error=error_msg)

        elif not self.user:
            self.redirect("/login")

        else:
            self.write("You do not have permission to edit this post")
