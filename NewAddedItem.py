import cgi
import os
import random

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Models import *

class NewAddedItem(webapp.RequestHandler):  #To show added item and option to add more
  def post(self):
      selectedCat = self.request.get('catName')
      loggedInUser = self.request.get('loggedInUser')
      
      newItem = AllItems()
      newItem.categoryName = self.request.get('catName')
      newItem.author = self.request.get('loggedInUser')
      newItem.itemName = self.request.get('itemName')
      newItem.put()
      
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", 
                                 selectedCat, loggedInUser)
      
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'loggedInUser': loggedInUser
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))