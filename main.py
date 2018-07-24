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


        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            #userquery=User.query(User.username==nickname).fetch()
            #print "query::::"
            #print userquery

            print("logged in")
            #if len(userquery)==0:

        else:
            login_url = users.create_login_url('/myhome')
            print ("logged out")


        template_vars = {
            "user": user,
            "nickname": nickname,
            "logout_url": logout_url,
            "login_url": login_url,
        }

        template = jinja_current_directory.get_template('templates/skeleton.html')
        self.response.write(template.render(template_vars))

class MyHomeHandler(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url": logout_url,
        }

        user = users.get_current_user()
        if(user):
            userquery=User.query(User.username==user.nickname()).fetch()
            if(len(userquery)==0):
                usertest=User(username=user.nickname(), recipe=["cake","bake","take"])
                key=usertest.put()
                print key

        template = jinja_current_directory.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

    def post(self):
        name=self.request.get("recipe_title")
        description=self.request.get("recipe_description")
        ingredients=self.request.get("recipe_ingredients")
        instructions=self.request.get("recipe_instructions")
        recipe=Recipe(name=name,description=description,ingredients=ingredients,
        instructions=instructions)
        key=recipe.put()
        print key


        template = jinja_current_directory.get_template('templates/myfeed.html')
        self.response.write(template.render())

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('about_us.html')
        self.response.write(template.render())

class MyFeedHandler(webapp2.RequestHandler):
    def get(self):


        template = jinja_current_directory.get_template('templates/myfeed.html')
        self.response.write(template.render())
#********

#********


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aboutus', MyHomeHandler),
    ('/myhome', MyHomeHandler),
    ('/myfeed', MyFeedHandler)
], debug=True)

class User(ndb.Model):
    username=ndb.StringProperty()
    recipe=ndb.StringProperty(repeated=True)

class Recipe(ndb.Model):
    name=ndb.StringProperty()
    description=ndb.StringProperty()
    ingredients=ndb.StringProperty()
    instructions=ndb.StringProperty()
