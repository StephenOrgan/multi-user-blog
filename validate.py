import os
import hashlib
import re
import jinja2
import hmac
import random 
from google.appengine.ext import db
from string import letters

# Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# Model Keys
def users_key(segment = 'default'):
    return db.Key.from_path('users', segment)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# Validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# Global functions

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

# Authentication
SECRET = 'imsosecret'

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def make_salt():
    return ''.join(random.choice(letters) for x in xrange(5))

def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)

def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(SECRET, val).hexdigest())

def check_secure_val(secure_val):
    if secure_val:
        val = secure_val.split('|')[0]
        if secure_val == make_secure_val(val):
            return val


