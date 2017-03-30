import hashlib
import os
import re
from string import letters

import webapp2
import jinja2
import hmac

from google.appengine.ext import db

SECRET = 'imsosecret'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

#BlogHandler
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # this makes hmac hash of name and sets it in the header as name=hash
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
        
    #if cookies and that cookie passes check_secure_val then return cookie_val
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # check the usercookie.  if exists store the user object in self.user
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class Signup(BlogHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done() #in the signup class run the done method

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        #make sure user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = "That user already exists"
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            set_secure_cookie(self.username)
            self.redirect('/welcome')



#define as a global definition as it is being used in templates
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s=%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('=')[0]
    if h == make_secure_val(val):
        return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (salt, h)

def valid_pw(name, pw, h):
    ###Your code here
    salt = h.split('|')[0]
    return h == make_pw_hash(name, pw, salt)


def users_key(group = 'default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    updated_at = db.DateTimeProperty(auto_now = True)

    # load the user from the db by ID. cls is like self and it stands for class. And has no colon.
    @classmethod
    def by_id(cls,uid):
        return User.get_by_id(uid, parent = users_key())

    
    #load user from db by filtering all users by that username
    @classmethod
    def by_name(cls,name):
        u = User.all().filter('name =', name).get()
        return u

    # this just creates the user it does not store in the db
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)






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




##### blog stuff

# this returns the key from the blog post.  The name allows us to have multiple blogs where default is the main schema?
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    updated_at = db.DateTimeProperty(auto_now = True)

    #this method replaces end lines with <br>.  It's called from permalink.html {{post.render() | safe}} 
    # which is then rendered to post.html and put into the base template
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

class BlogFront(BlogHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created_at desc limit 10")
        self.render('front.html', posts = posts)

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)#figure out what parent does
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)



###### Unit 2 HW's
class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)

class Unit3Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')


class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13', Rot13),
                               ('/signup', Register),
                               ('/welcome', Unit3Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ],
                              debug=True)
