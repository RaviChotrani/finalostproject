import cgi
import os
import random
import urllib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Models import *

class AllItemsForUser(webapp.RequestHandler):  # Edit Existing Category : i.e; This supports only addition of items to the category
  def post(self):
      selectedCat = self.request.get('catName')
      loggedInUser = self.request.get('loggedInUser')
      logout = self.request.get('logout')
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, loggedInUser)
      expTimeHH = self.request.get('expTimeHH')
      expTimeMM = self.request.get('expTimeMM')
      expTimeSS = self.request.get('expTimeSS')
 
      #if expTimeMM:
      allExpTime = db.GqlQuery("SELECT * FROM ExpirationTime WHERE categoryName = :1 AND loggedInUser = :2", 
                                 selectedCat, loggedInUser)
      results6 = allExpTime.fetch(100)
      db.delete(results6)  
      
      if (expTimeHH != "0" or expTimeMM != "0" or expTimeSS != "0"):         
          newExpTime = ExpirationTime()
          newExpTime.categoryName = selectedCat
          newExpTime.loggedInUser = loggedInUser
          newExpTime.expHH = expTimeHH
          newExpTime.expMM = expTimeMM 
          newExpTime.expSS = expTimeSS
          newExpTime.put()
     
      allExpTime = db.GqlQuery("SELECT * FROM ExpirationTime WHERE categoryName = :1 AND loggedInUser = :2", 
                                 selectedCat, loggedInUser)
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'loggedInUser': loggedInUser,
        'logout': logout,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))
 