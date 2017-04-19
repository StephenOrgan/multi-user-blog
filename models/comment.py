from google.appengine.ext import db
from validate import render_str
from models.user import User
from models.post import Post


class Comment(db.Model):
    content = db.TextProperty(required=True)
    post = db.ReferenceProperty(Post, required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, required=True)

    def render_comment(self):
        """ Display comments content comment.html template.  TO DO:
        remove as this has been deprecated """
        return render_str("comment.html", c=self, user=self.user)

    def format_content(self):
        """ Display comment content in the show_comment.html template. Linebreaks
        will be replaced with a <br> """
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('show_comment.html', c=self)
