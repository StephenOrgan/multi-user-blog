from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.like import Like as LikeModel

class Post(BlogHandler):
    def get(self, post_id):
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)
        comments = db.GqlQuery(
            "select * from Comment where ancestor is :1 order by created desc limit 10", postkey)
        likes = db.GqlQuery(
            "select * from Like where ancestor is :1", postkey)

        if not post:
            self.error(404)
            return

        
        self.render("permalink.html", post = post, comments = comments, likes = likes)