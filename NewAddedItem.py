import cgi
import os
import random
import cgi, os
import urllib

from xml.dom.minidom import parseString
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
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
      logout = self.request.get('logout')
      itemName = self.request.get('itemName')
      deletedItems = self.request.get_all('deletedItems')
      
      if deletedItems:
          for item in deletedItems:
              deleteFromAllItems = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2 AND itemName = :3", 
                                     selectedCat, loggedInUser, item)
              results = deleteFromAllItems.fetch(100)
              db.delete(results)
          
          for item in deletedItems:
              deleteFromAllComments = db.GqlQuery("SELECT * FROM AllComments WHERE categoryName = :1 AND itemName = :2", 
                                     selectedCat, item)
              results = deleteFromAllComments.fetch(100)
              db.delete(results)
          
          for item in deletedItems:
              deleteFromAllWinners =  db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND winner = :2", 
                                     selectedCat, item)
              results = deleteFromAllWinners.fetch(100)
              db.delete(results)
              
          for item in deletedItems:
              deleteFromAllLosers =  db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND loser = :2", 
                                     selectedCat, item)
              results = deleteFromAllLosers.fetch(100)
              db.delete(results)   
      
      if itemName:       
          itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", 
                                     selectedCat, loggedInUser)
          
          isItemPresent = "F"
          for itemInfo in itemsForUser:
             if itemName == itemInfo.itemName:
                isItemPresent = "T"
                break
                   
          if isItemPresent == "F":     
              newItem = AllItems()
              newItem.categoryName = selectedCat
              newItem.author = loggedInUser
              newItem.itemName = itemName
              newItem.put()

      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", 
                                 selectedCat, loggedInUser)
      
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'loggedInUser': loggedInUser,
        'logout': logout
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)
