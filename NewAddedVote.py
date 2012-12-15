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

class NewAddedVote(webapp.RequestHandler):  #To update Vote casted and option to vote again on same category
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      logout = self.request.get('logout')
      selectedCat = self.request.get('selectedCat')
      selectedItem = self.request.get('selectedItem')
      username = self.request.get('username')
      previousitem1 = self.request.get('item1')
      previousitem2 = self.request.get('item2')
      previousComment1 = self.request.get('previousComment1')
      previousComment2 = self.request.get('previousComment2')
      appendComment1 = self.request.get('appendComment1')
      appendComment2 = self.request.get('appendComment2')
      btnClicked = self.request.get('btn')
      
      vote_cast = ""
      if btnClicked != "skip":
          newVote = AllVotes()
          newVote.categoryName = self.request.get('selectedCat')
          newVote.author = self.request.get('username')
          if selectedItem == previousitem1:
              vote_cast = "Y"
              newVote.winner = selectedItem
              newVote.loser = previousitem2
              newVote.put()
          elif selectedItem == previousitem2:
              vote_cast = "Y"
              newVote.winner = selectedItem
              newVote.loser = previousitem1
              newVote.put()
          else:
              # Do Nothing
              selectedItem = ""         
      
      if previousComment1 != None: 
          if previousComment1 != "":
              if appendComment1 == "T": 
                  newComment = AllComments()
                  newComment.loggedInUser = loggedInUser
                  newComment.categoryName = selectedCat
                  newComment.itemName = previousitem1
                  newComment.itemComment = previousComment1
                  newComment.put()
          
      if previousComment2 != None:
          if previousComment2 != "":
              if appendComment2 == "T":
                  newComment = AllComments()
                  newComment.loggedInUser = loggedInUser
                  newComment.categoryName = selectedCat
                  newComment.itemName = previousitem2
                  newComment.itemComment = previousComment2
                  newComment.put()
              
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, username)
      count = itemsForUser.count()
      error_msg = ""
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
      
      newComment1 = ""
      newComment2 = ""
      for comments in allComments:
          if comments.itemName == item1:
             newComment1 = comments.itemComment
          if comments.itemName == item2:
              newComment2 = comments.itemComment
                         
      template_values = {
        'vote_cast': vote_cast,
        'loggedInUser': loggedInUser,
        'selectedItem': selectedItem,
        'item1': item1,
        'item2': item2,
        'previousComment1': newComment1,
        'previousComment2': newComment2,
        'selectedCat': selectedCat,
        'author': username,
        'logout': logout
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
      self.response.out.write(template.render(path, template_values))     
