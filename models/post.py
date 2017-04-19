from google.appengine.ext import db
from validate import *
from models.user import User


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    like_count = db.IntegerProperty(required=True, default=0)
    comment_count = db.IntegerProperty(required=True, default=0)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)

    """ This method renders the post in post.html and replaces
    linebreaks with <br>. """
    def render(self, current_user_id):
        userkey = db.Key.from_path('User', int(self.user_id),
                                   parent=users_key())
        user = db.get(userkey)

        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html",
                          p=self, current_user_id=current_user_id,
                          username=user.name,
                          user_id=self.user_id,
                          like_count=self.like_count,
                          comment_count=self.comment_count)

    """ Return the user associated with a particular user id.  TO DO:
    remove as this has been deprecated """

    def by_user_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    """ Return the Post associated with a particular post id.  TO DO:
    remove as this has been deprecated """

    @classmethod
    def by_id(cls, pid):
        return Post.get_by_id(pid, parent=blog_key())
