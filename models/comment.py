from google.appengine.ext import db

class Comment(db.Model): 
	content = db.TextProperty(required=True) 
	user_id = db.IntegerProperty(required=True)
	post_id = db.IntegerProperty(required=True)
	created_at = db.DateTimeProperty(auto_now_add=True) 
	updated_at = db.DateTimeProperty(auto_now=True)

	
	def render(self, current_user_id):
		#userkey = db.Key.from_path('User', int(self.user_id), parent = users_key())
		#user = db.get(userkey)	
		
		self._render_comment = self.content.replace('\n', '<br>')
		return render_str("comment.html", c = self, current_user_id = current_user_id)