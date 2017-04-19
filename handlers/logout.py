from handlers.bloghandler import BlogHandler


class Logout(BlogHandler):
    """ Run the logout function in bloghandler and redirect the user
    back to the homepage """
    def get(self):
        self.logout()
        self.redirect('/')
