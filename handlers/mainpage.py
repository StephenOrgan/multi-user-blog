from handlers.bloghandler import BlogHandler
from validate import *

class MainPage(BlogHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    visits = 0
    visit_cookie_str = self.request.cookies.get('visits')
    if visit_cookie_str:
        cookie_val = check_secure_val(visit_cookie_str)
        if cookie_val:
            visits = int(cookie_val)

    visits += 1

    new_cookie_val = make_secure_val(str(visits))

    self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)

    self.write("You've been here %s times!" % visits)