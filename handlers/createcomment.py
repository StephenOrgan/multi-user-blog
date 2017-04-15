from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.comment import Comment

class CreateComment(BlogHandler):

    def get(self, post_id, user_id):
        if not self.user:
            self.render('/login')
        else:
            self.render("create-comment.html")

    def post(self, post_id, user_id):
        if not self.user:
            self.redirect('/login')

        content = self.request.get('content')
        user_name = self.user.name
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        c = Comment(parent=postkey, user_id=int(user_id), content=content, post_id=int(post_id))
        
        c.put()

        self.redirect('/' + post_id)