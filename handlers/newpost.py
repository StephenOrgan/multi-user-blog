from handlers.bloghandler import BlogHandler
from models.post import Post
from validate import *


class NewPost(BlogHandler):
    
    def get(self):
        """ If the user is signed in, render newpost.html, otherwise pass users
        to the basetemplate with an error message """
        if self.user:
            self.render("newpost.html")

        else:
            error_msg = "You need to be logged in to author a post"
            self.render("base.html", error=error_msg)

    def post(self):
        """ If subject and content is present create the post in the database.
        Otherwise user sees the newpost form with an appropriate error message. """
        if not self.user:
            return self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content,
                     user_id=self.user.key().id())

            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "Both a title and content is required to create a post"

            self.render("newpost.html",
                        subject=subject, content=content, error=error)
