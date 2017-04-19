from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *


class BlogFront(BlogHandler):

    
    def get(self):
        """ Get the most recent 10 posts and render them on front.html """
        posts = db.GqlQuery(
            "select * from Post order by created_at desc limit 10")
        self.render('front.html', posts=posts)
