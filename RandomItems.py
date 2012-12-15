import cgi
import os
import random
import datetime

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Models import *

class RandomItems(webapp.RequestHandler):
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      logout = self.request.get('logout')
      catAndUser = self.request.get('catName')
      x = catAndUser.split(',')
      selectedCat = x[0].strip()
      username = x[1].strip()
      
      now = datetime.datetime.now()
      catExpTime = db.GqlQuery("SELECT * FROM ExpirationTime WHERE categoryName = :1 AND loggedInUser = :2", selectedCat, username)
      rowCount = catExpTime.count()
      isCatExpired = ""
      if rowCount > 0:
          for category in catExpTime:
              expHH = category.expHH
              expMM = category.expMM
              expSS = category.expSS
              break
          
          isCatExpired = "F"
          if now.hour < int(expHH):
              isCatExpired = "F"
          elif now.hour > int(expHH):
              isCatExpired = "T"
          else:       
              if now.minute < int(expMM):
                  isCatExpired = "F"
              elif now.minute > int(expMM):    
                  isCatExpired = "T"
              else:
                  if now.second < int(expSS):
                    isCatExpired = "F"
                  else:
                    isCatExpired = "T"
      
      categ_expired = ""              
      if isCatExpired == "T":
          categ_expired = "T"
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'loggedInUser': loggedInUser,
            'categ_expired': categ_expired,
            'vote_page': "Y",
            'expHH': expHH,
            'expMM': expMM,
            'expSS': expSS,
            'logout': logout
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
      
      else:                         
                                  
          itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, username)
          
          count = itemsForUser.count()
          error_msg = ""
          if count < 2:
              error_msg = "Y"
              allCategories = db.GqlQuery("SELECT * FROM AllCategories")
              template_values = {
                'allCategories': allCategories,
                'loggedInUser': loggedInUser,
                'error_msg': error_msg,
                'logout': logout
              }
    
              path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
              self.response.out.write(template.render(path, template_values))
              
          else:    
              if count == 2:
                  i = 0
                  j = 1
              else:        
                  i = random.randint(0, count-1)
                  j = random.randint(0, count-1)
                  while i == j:
                      i = random.randint(0, count-1)
                      j = random.randint(0, count-1)
              
              itemCount = 0
               
              item1 = ""
              item2 = ""    
              for itemInfo in itemsForUser:
                  if itemCount == i:
                      item1 = itemInfo.itemName
                  if itemCount == j:
                      item2 = itemInfo.itemName
                  itemCount+= 1    
                         
              allComments = db.GqlQuery("SELECT * FROM AllComments WHERE categoryName = :1 AND loggedInUser = :2 "+
                                        " AND itemName IN (:3, :4) ", selectedCat, loggedInUser, item1, item2)
              
              previousComment1 = ""
              previousComment2 = ""
              for comments in allComments:
                  if comments.itemName == item1:
                     previousComment1 = comments.itemComment
                  if comments.itemName == item2:
                      previousComment2 = comments.itemComment
                         
              template_values = {
                'item1': item1,
                'item2': item2,
                'previousComment1': previousComment1,
                'previousComment2': previousComment2,
                'loggedInUser': loggedInUser,
                'selectedCat': selectedCat,
                'author': username,
                'logout': logout
                
              }
        
              path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
              self.response.out.write(template.render(path, template_values))     
