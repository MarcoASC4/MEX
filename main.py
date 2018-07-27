import jinja2
import os
import webapp2
from datetime import datetime
import cgi
import urllib
#from pytz import timezone
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
#from PIL import Image


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
            #logout_url = users.create_logout_url('/')
            #userquery=User.query(User.username==nickname).fetch()
            #print "query::::"
            #print userquery
            self.redirect('/myhome')

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



class PostHandler(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')
        user = users.get_current_user()
        userproperty=User.query(User.username==user.nickname()).fetch()[0]

        if userproperty.fullname is None:
            self.redirect('/createprofile')

        template_vars = {
            "logout_url": logout_url,
        }
        template = jinja_current_directory.get_template('templates/post.html')
        self.response.write(template.render(template_vars))

    def post(self):
        name=self.request.get("recipe_title")
        description=self.request.get("recipe_description")
        ingredients=self.request.get("recipe_ingredients")
        instructions=self.request.get("recipe_instructions")
        #fmt = "%a %B %d, %Y - %I:%M %p"
        #tz = timezone('America/New_York')
        # Current time in UTC
        #now_utc = datetime.now(tz)
        #print now_utc

        # Convert to US/Pacific time zone
        #now_time = now_utc.astimezone(timezone('US/Eastern'))
        #print now_time
        # currenttime = now_time.strftime(fmt)
        #datetime_in_eastern=date_time.datetime.astimezone(timezone('US/Eastern'))
        #date_time=datetime.datetime.now()
        # printdatetime = date_time.strftime("%a, %b %d, - %Y %I:%M: %p ")

        user = users.get_current_user()
        nickname = user.nickname()
        #print user


        userproperty=User.query(User.username==user.nickname()).fetch()[0]

        #print userproperty

        pic = self.request.get("fileupload")
        recipe=Recipe(name=name,description=description,ingredients=ingredients,
                instructions=instructions, owner=userproperty.key, datetime=datetime.now(),
                picture=images.resize(pic,500,1000))
        key=recipe.put()
        #print key



        userproperty.recipes.append(key)
        # print(userproperty.recipes)
        userproperty.put()
        get_back_user_recipes = Recipe.query(Recipe.owner==userproperty.key).fetch()


        print get_back_user_recipes

        retrieved_recipes=[]
        image_url=[]


        get_back_user_recipes=Recipe.query(Recipe.owner==userproperty.key).fetch()

        image_url=[]
        retrieved_recipes = []


        for recipe in get_back_user_recipes:
            retrieved_recipes.append(recipe)
            image_url.append(recipe.key.urlsafe())


        #print(recipes_list)

        #users_list = []
        #for userproperty.key in users:
        #    users_list.append(userproperty.key.get())

        #print recipes_list


        #print recipes_list.sort(key=lambda r: r.datetime)

        template_vars={
            "username": userproperty.username,
            "recipes": retrieved_recipes,
            "nickname": nickname,
            "fullname": userproperty.fullname,
            "bio": userproperty.bio,
            "urls": image_url,
            "pfp":userproperty.key.urlsafe()
        }

        #count=0
        #print userproperty.recipe.name
        #userproperty.recipe.append(key).put()
        template = jinja_current_directory.get_template('templates/myprofile.html')
        self.response.write(template.render(template_vars))
        #self.redirect('/myprofile')
    #    for x,y in template_vars.items():
    #        print (x,y)

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        userproperty=User.query(User.username==user.nickname()).fetch()[0]


        #assign these to something so the python runs no matter what
        logout_url = None

        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            print nickname



        template_vars = {
            "user": user,
            "logout_url": logout_url,
            "profile": userproperty.fullname,
            #"urls":image_url
            }

        template = jinja_current_directory.get_template('templates/aboutus.html')
        self.response.write(template.render(template_vars))

class MyHomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()


        #assign these to something so the python runs no matter what
        logout_url = None

        if(user):
            userquery=User.query(User.username==user.nickname()).fetch()
            if(len(userquery)==0):
                usertest=User(username=user.nickname(), recipes=[])
                key=usertest.put()
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            #print nickname
        #userproperty=User.query(User.username==user.nickname()).fetch()[0]


        template_vars = {
            "user": user,
            "logout_url": logout_url,
            #"profile": userquery.fullname,
            }
        template = jinja_current_directory.get_template('templates/home.html')
        self.response.write(template.render(template_vars))


class MyFeedHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        #assign these to something so the python runs no matter what
        logout_url = None

        if user:
            nickname = user.nickname()
            userproperty=User.query(User.username==user.nickname()).fetch()[0]
            logout_url = users.create_logout_url('/')
            print nickname

        if userproperty.fullname is None:
            self.redirect('/createprofile')

        get_back_all_recipes = Recipe.query().fetch()

        #print get_back_all_recipes

        all_retrieved_recipes=[]
        owners=[]
        image_url=[]


        for recipe in get_back_all_recipes:
            all_retrieved_recipes.append(recipe)
            print ("testing2")
            image_url.append(recipe.key.urlsafe())
            print (recipe.owner)
            #owners.append(recipe.owner)
            owner = recipe.owner.get()
            print owner
            owners.append(owner)

        print owners
            #name_key = recipe.owner.get()
            #recipe_maker = name_key.fullname
        #for recipe in get_back_all_recipes:
        #    username = recipe.owner
        #print "testing"
        #print all_retrieved_recipes
        #print owners

        template_vars = {
            "user": user,
            "logout_url": logout_url,
            "username": userproperty.username,
            "recipes": all_retrieved_recipes,
            "owner": owners,
            "urls": image_url,
            }

        template = jinja_current_directory.get_template('templates/myfeed.html')
        self.response.write(template.render(template_vars))

class MyProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = None

        if user:
            nickname = user.nickname()
            userproperty=User.query(User.username==user.nickname()).fetch()[0]
            logout_url = users.create_logout_url('/')
            print nickname

        if userproperty.fullname is None:
            self.redirect('/createprofile')

        get_back_user_recipes = Recipe.query(Recipe.owner==userproperty.key).fetch()

        print get_back_user_recipes

        retrieved_recipes=[]
        image_url=[]

        for recipe in get_back_user_recipes:
            retrieved_recipes.append(recipe)
            image_url.append(recipe.key.urlsafe())

        #userfull = userproperty.key.get()

        print "neeraj"
        print image_url



        template_vars = {
            "user": user,
            "logout_url": logout_url,
            #"username": userproperty.username,
            "nickname": nickname,
            "recipes": retrieved_recipes,
            "fullname": userproperty.fullname,
            "bio": userproperty.bio,
            "urls": image_url,
            "pfp": userproperty.key.urlsafe()
            }
        template = jinja_current_directory.get_template('templates/myprofile.html')
        self.response.write(template.render(template_vars))



class Image(webapp2.RequestHandler):
    def get(self):
        greeting_key = ndb.Key(urlsafe=self.request.get('img_id'))
        greeting = greeting_key.get()
        if greeting.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.picture)
        else:
            self.response.out.write('No image')

class CreateProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')

        if user:
            nickname = user.nickname()
            userproperty=User.query(User.username==user.nickname()).fetch()[0]
            logout_url = users.create_logout_url('/')
        #if(user):
        #    nickname = user.nickname()
        #    userquery=User.query(User.username==user.nickname()).fetch()
        #    if(len(userquery)==0):
        #        usertest=User(username=user.nickname(), recipes=[])
        #        user=usertest.put()

        template_vars = {
            "logout_url": logout_url,
            "profile": userproperty.fullname,
        }

        template = jinja_current_directory.get_template('templates/createprofile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        user = users.get_current_user()
        fullname = self.request.get("full_name")
        bio = self.request.get("bio")

        #assign these to something so the python runs no matter what
        logout_url = None


        if user:
            nickname = user.nickname()
            userproperty=User.query(User.username==user.nickname()).fetch()[0]
            logout_url = users.create_logout_url('/')
            print nickname

        img=self.request.get('pfpupload')
        img=images.resize(img,100,100)

        #fullname = self.request.get("full_name")
        #bio = self.request.get("bio")

        userfull = userproperty.key.get()
        userfull.fullname = fullname
        userfull.bio = bio
        userfull.picture=img
        userfull.put()



        get_back_user_recipes = Recipe.query(Recipe.owner==userproperty.key).fetch()

        print get_back_user_recipes

        retrieved_recipes=[]
        image_url=[]

        for recipe in get_back_user_recipes:
            retrieved_recipes.append(recipe)
            image_url.append(recipe.key.urlsafe())




        #profile = User(username=nickname, fullname = self.request.get("full_name"), bio = self.request.get("bio"), recipes=retrieved_recipes)

        #retrieved_profiles = User.query().fetch()

        #profiles_list = []

        #for profile in retrieved_profiles:
        #    profiles_list.append(profile)

        template_vars = {
            "user": user,
            "logout_url": logout_url,
            "recipes": retrieved_recipes,
            "fullname": fullname,
            "bio": bio,
            "urls": image_url,
            "pfp": userfull.key.urlsafe()
        }

        template = jinja_current_directory.get_template('templates/myprofile.html')
        self.response.write(template.render(template_vars))

class ExploreHandler(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')


        user = users.get_current_user()

        if(user):
            userquery=User.query(User.username==user.nickname()).fetch()
            if(len(userquery)==0):
                usertest=User(username=user.nickname(), recipes=[], picture=None)
                key=usertest.put()
            userproperty=User.query(User.username==user.nickname()).fetch()[0]



        if userproperty.fullname is None:
            self.redirect('/createprofile')

        get_all_users = User.query().fetch()
            #print get_all_users

        users_list = []

        for user in get_all_users:
            users_list.append(user)
            print "TESTING"
        #print users_list

        #for user in users_list:
        #    print user.fullname

        template_vars = {
            "logout_url": logout_url,
            "users_list": users_list,
        }

        template = jinja_current_directory.get_template('templates/explore.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/myhome', MyHomeHandler),
    ('/aboutus', AboutUsHandler),
    ('/post', PostHandler),
    ('/myfeed', MyFeedHandler),
    ('/myprofile', MyProfileHandler),
    ('/img',Image),
    ('/createprofile', CreateProfileHandler),
    ('/explore', ExploreHandler),

], debug=True)

class User(ndb.Model):
    username=ndb.StringProperty()
    fullname=ndb.StringProperty()
    bio=ndb.TextProperty()
    recipes=ndb.KeyProperty(kind="Recipe", repeated=True)
    picture=ndb.BlobProperty()

class Recipe(ndb.Model):
    name=ndb.StringProperty()
    description=ndb.StringProperty()
    ingredients=ndb.StringProperty()
    instructions=ndb.StringProperty()
    owner=ndb.KeyProperty(kind="User")
    datetime=ndb.DateTimeProperty(auto_now=True)
    picture=ndb.BlobProperty()
