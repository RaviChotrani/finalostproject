import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Models import *

class FirstPage(webapp.RequestHandler):
  def post(self):
      initChoice = self.request.get('firstChoice')
      loggedInUser = self.request.get('loggedInUser')  
      if initChoice == "opt1":    # Vote on Existing Category
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'loggedInUser': loggedInUser
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt2":    # Edit existing Category 
         categsForUser = db.GqlQuery("SELECT * FROM AllCategories where author = :1", loggedInUser)
         
         template_values = {
            'categsForUser': categsForUser,
            'loggedInUser' : loggedInUser
         }

         path = os.path.join(os.path.dirname(__file__), 'templates/UserCategs.html')
         self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt3":    # Create a new Category
          category = AllCategories()
          #self.response.headers['Content-Type'] = 'text/html'
          loggedInUser = self.request.get('loggedInUser')
          #self.response.out.write('Hii')
          #self.response.out.write(username)
          #self.response.out.write('Hello')
          category.author = self.request.get('loggedInUser')
          category.categoryName = self.request.get('catName')
          category.put()
          template_values = {
             'categoryAdded' : "Y",
             'loggedInUser' : loggedInUser
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt4":    # View Results
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt4': "Y",
            'loggedInUser' : loggedInUser
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt5":    # eXPORT XML
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt5': "Y",
            'loggedInUser' : loggedInUser
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
 