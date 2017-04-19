from handlers.bloghandler import BlogHandler


class Logout(BlogHandler):
    
    def get(self):
        """ Run the logout function in bloghandler and redirect the user
        back to the homepage """
        self.logout()
        self.redirect('/')
