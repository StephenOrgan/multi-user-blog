from handlers.bloghandler import BlogHandler
from models.post import Post
from validate import *

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")

        else:
            error_msg = "You need to be logged in to author a post"
            self.render("base.html", error = error_msg)

    def post(self):
        if not self.user:
            self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, user_id = self.user.key().id())
            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "Both a title and content is required to create a post"
            self.render("newpost.html", subject=subject, content=content, error=error)