import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb



jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        #assign these to something so the python runs no matter what
        nickname = None
        logout_url = None
        login_url = None

        added=False

        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')

            '''if added==False:
                usertest=User(username=str(user), recipe=["cake","bake"])
                key=usertest.put()
                print key
                added=True'''
        else:
            login_url = users.create_login_url('/')

        template_vars = {
            "user": user,
            "nickname": nickname,
            "logout_url": logout_url,
            "login_url": login_url,
        }

        template = jinja_current_directory.get_template('templates/skeleton.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

class User(ndb.Model):
    username=ndb.StringProperty()
    recipe=ndb.StringProperty(repeated=True)
