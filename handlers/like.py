from google.appengine.ext import db
from handlers.bloghandler import BlogHandler
from validate import *
from models.like import Like as LikeModel


class LikeHandler(BlogHandler):

    def get(self, post_id):
        """ If the user is signed in and has authored the post render the
        basetemplate with an error message as they can't like their own posts.

        Pass the user to the sign in page if the user isn't signed in.

        Lookup whether the user has liked the post.  If liked, redirect the user
        to the post page.  Otherwise a new like can be recorded in the db and
        increment the like_count in the post model. """
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)

        if post is not None:
            if self.user and self.user.key().id() == post.user_id:
                error = "Sorry, you cannot like your own post."
                self.render('base.html', error=error)
            elif not self.user:
                self.redirect('/login')
            else:
                user_id = self.user.key().id()
                post_id = post.key().id()

                liked = LikeModel.all().filter(
                    'user_id =', user_id).filter('post_id =', post_id).get()

                if liked:
                    self.redirect('/' + str(post.key().id()))

                else:
                    like = LikeModel(parent=postkey,
                                     user_id=self.user.key().id(),
                                     post_id=post.key().id())

                    post.like_count += 1

                    like.put()
                    post.put()

                    self.redirect('/' + str(post.key().id()))


class UnlikeHandler(BlogHandler):

    def get(self, post_id):
        """ If the user is signed in and has authored the post render the
        basetemplate with an error message as they can't unlike their own posts.

        Pass the user to the sign in page if the user isn't signed in.

        Lookup whether the user has liked the post.  If liked, delete the like
        from the db and deincrement the like_count in the post model """
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(postkey)

        if post is not None:
            if self.user and self.user.key().id() == post.user_id:
                self.write("You cannot unlike your own post")
            elif not self.user:
                self.redirect('/login')
            else:
                user_id = self.user.key().id()
                post_id = post.key().id()

                l = LikeModel.all().filter(
                    'user_id =', user_id).filter('post_id =', post_id).get()

                if l:
                    l.delete()
                    post.like_count -= 1
                    post.put()

                    self.redirect('/' + str(post.key().id()))
                else:
                    self.redirect('/' + str(post.key().id()))
