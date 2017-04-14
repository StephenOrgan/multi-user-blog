from google.appengine.ext import db
from validate import *

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    like_count = db.IntegerProperty(required = True, default = 0)
    created_at = db.DateTimeProperty(auto_now_add = True)
    updated_at = db.DateTimeProperty(auto_now = True)
    user_id = db.IntegerProperty(required = True)

    #this method replaces end lines with <br>.  It's called from permalink.html {{post.render() | safe}} 
    # which is then rendered to post.html and put into the base template
    def render(self, current_user_id):
        userkey = db.Key.from_path('User', int(self.user_id), parent = users_key())
        user = db.get(userkey)

        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self, current_user_id = current_user_id, username = user.name)

    @classmethod
    def by_id(cls, uid):
        return Post.get_by_id(uid, parent=blog_key())


