from google.appengine.ext import db

class Comment(db.Model): 
	content = db.TextProperty(required=True) 
	user_id = db.IntegerProperty(required=True)
	post_id = db.IntegerProperty(required=True)
	created_at = db.DateTimeProperty(auto_now_add=True) 
	updated_at = db.DateTimeProperty(auto_now=True)
