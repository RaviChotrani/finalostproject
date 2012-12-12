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
      logout = self.request.get('logout')  
      if initChoice == "opt1":    # Vote on Existing Category
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'loggedInUser': loggedInUser,
            'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt2":    # Edit existing Category 
         categsForUser = db.GqlQuery("SELECT * FROM AllCategories where author = :1", loggedInUser)
         
         template_values = {
            'categsForUser': categsForUser,
            'loggedInUser' : loggedInUser,
            'logout': logout
         }

         path = os.path.join(os.path.dirname(__file__), 'templates/UserCategs.html')
         self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt3":    # Create a new Category
          loggedInUser = self.request.get('loggedInUser')
          categoryName = self.request.get('catName')
          allCategories = db.GqlQuery("SELECT * FROM AllCategories where author = :1", loggedInUser)
          isCatPresent = "F"
          for categ in allCategories:
              if categoryName == categ.categoryName:
                   isCatPresent = "T"
                   break
               
          if isCatPresent == "F":     
              category = AllCategories()
              category.author = loggedInUser
              category.categoryName = categoryName
              category.put()
              
          template_values = {
             'categoryAdded' : "Y",
             'loggedInUser' : loggedInUser,
             'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt4":    # View Results
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt4': "Y",
            'loggedInUser' : loggedInUser,
            'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt5":    # eXPORT XML
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt5': "Y",
            'loggedInUser' : loggedInUser,
            'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt6":    # Search Item / Category
          loggedInUser = self.request.get('loggedInUser')
          searchElement = self.request.get('searchElement')
          resultListFound = []
          count = 0
          allItems = db.GqlQuery("SELECT * FROM AllItems")
          for eachItem in allItems:
              resultStr = ""
              if searchElement in eachItem.itemName:
                 resultStr = "Matching Item name: "+ eachItem.itemName+" found in "+eachItem.categoryName+" owned by "+eachItem.author
                 resultListFound.append(resultStr)
                 count += 1
              else:
                  if searchElement in eachItem.categoryName:
                      resultStr = "Matching Category name: "+eachItem.categoryName+" owned by "+eachItem.author
                      resultListFound.append(resultStr)
                      count += 1

           
          
          template_values = {
             'loggedInUser' : loggedInUser,
             'resultListFound' : resultListFound,
             'searchElement': searchElement,
             'count': count,
             'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/SearchPage.html')
          self.response.out.write(template.render(path, template_values))       
 