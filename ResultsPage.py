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

class ResultsPage(webapp.RequestHandler):  #View Results on a given category
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      categoryName = self.request.get('catName')
      username = self.request.get('username')
      
      itemsofCateg = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", categoryName, username)
      votesofCateg = db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND author = :2", categoryName, username)
      
      for itemCat in itemsofCateg:
          item = itemCat.itemName
          userList = []
          userComment = []
          allComments = db.GqlQuery("SELECT * FROM AllComments WHERE categoryName = :1 AND itemName = :2", categoryName, item)
          for comment in allComments:
              userList.append(comment.loggedInUser)
              userComment.append(comment.itemComment)
              
          winCount = 0
          lossCount = 0
          percent = 0
          for voteCat in votesofCateg:
              winner = voteCat.winner
              loser = voteCat.loser
              if item == winner:
                  winCount+= 1
              if item == loser:
                  lossCount+= 1
                      
          if winCount == 0 and lossCount == 0:
              percent = 0
          else:
              sum = winCount + lossCount
              div = float(winCount)/sum
              percent = div * 100
                  
          newResult = AllResults()
          newResult.categoryName = categoryName
          newResult.author = username
          newResult.itemName = item
          newResult.winCount = winCount
          newResult.lossCount = lossCount
          newResult.percentWin = int(percent)
          newResult.userList = userList
          newResult.userComment = userComment
          newResult.put()
                      
      allResults = db.GqlQuery("SELECT * FROM AllResults WHERE categoryName = :1 AND author = :2 ORDER BY percentWin DESC ", categoryName, username)
      
      template_values = {
        'loggedInUser': loggedInUser,                 
        'allResults': allResults,
        'categoryName': categoryName,
        'author': username
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/ResultsPage.html')
      self.response.out.write(template.render(path, template_values))
      
