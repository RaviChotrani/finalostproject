import cgi
import os
import random

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class AllCategories(db.Model):
  categoryName = db.StringProperty()
  author = db.StringProperty()

class AllItems(db.Model):
  categoryName = db.StringProperty()
  author = db.StringProperty()
  itemName = db.StringProperty()
  
class AllVotes(db.Model):
  categoryName = db.StringProperty()
  author = db.StringProperty()
  winner = db.StringProperty()
  loser = db.StringProperty()

class AllResults(db.Model):
  categoryName = db.StringProperty()
  author = db.StringProperty()
  itemName = db.StringProperty()
  winCount = db.IntegerProperty()
  lossCount = db.IntegerProperty()
  percentWin = db.IntegerProperty()
  
class AllComments(db.Model):
  loggedInUser = db.StringProperty()
  categoryName = db.StringProperty()
  itemName = db.StringProperty()
  itemComment = db.StringProperty()
  
# Use this for Unit Testing
      #self.response.headers['Content-Type'] = 'text/html'
      #self.response.out.write('Hii')
      #self.response.out.write(selectedCat)
      #self.response.out.write(username)
      #self.response.out.write('Hello')

class Login(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <html>
    <body>
    <form action="/welcome" method="post">
      Username: <input type="text" name="loggedInUser"><br>
      <button type="submit" value="Login">Submit</button>
      <button type="reset" value="Reset">Reset</button>
    </form>
    </body>
    </html>""")
    
class Welcome(webapp.RequestHandler):
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      '''
      Small utility to clear records -- Uncomment only to clear records and then comment back
      q1 = db.GqlQuery("SELECT * FROM AllCategories")
      results1 = q1.fetch(10)
      db.delete(results1)
      q2 = db.GqlQuery("SELECT * FROM AllItems")
      results2 = q2.fetch(10)
      db.delete(results2)
      q3 = db.GqlQuery("SELECT * FROM AllVotes")
      results3 = q3.fetch(10)
      db.delete(results3)
      '''
      # Deleting all Records of AllResults to avoid multiple record entries
      q4 = db.GqlQuery("SELECT * FROM AllResults")
      results4 = q4.fetch(1000)
      db.delete(results4)
      
      template_values = {
        'loggedInUser': loggedInUser,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
      self.response.out.write(template.render(path, template_values))

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
          username = self.request.get('username')
          #self.response.out.write('Hii')
          #self.response.out.write(username)
          #self.response.out.write('Hello')
          category.author = self.request.get('username')
          category.categoryName = self.request.get('catName')
          category.put()
          template_values = {
             'author': username,
             'categoryAdded' : "Y"
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt4":    # View Results
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt4': "Y"
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
          
      if initChoice == "opt5":    # eXPORT XML
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories,
            'opt5': "Y"
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
               
class RandomItems(webapp.RequestHandler):
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      selectedCat = self.request.get('catName')
      username = self.request.get('username')
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, username)
      count = itemsForUser.count()
      error_msg = ""
      if count < 2:
          error_msg = "Y"
      elif count == 2:
          i = 1
          j = 2
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
        'author': username
        
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
      self.response.out.write(template.render(path, template_values))     
      
      
class AllItemsForUser(webapp.RequestHandler):  # Edit Existing Category : i.e; This supports only addition of items to the category
  def post(self):
      selectedCat = self.request.get('catName')
      loggedInUser = self.request.get('loggedInUser')
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, loggedInUser)
      
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'loggedInUser': loggedInUser
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))
      

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
      
class NewAddedVote(webapp.RequestHandler):  #To update Vote casted and option to vote again on same category
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      selectedCat = self.request.get('selectedCat')
      selectedItem = self.request.get('selectedItem')
      username = self.request.get('username')
      previousitem1 = self.request.get('item1')
      previousitem2 = self.request.get('item2')
      previousComment1 = self.request.get('previousComment1')
      previousComment2 = self.request.get('previousComment2')
      
      newVote = AllVotes()
      newVote.categoryName = self.request.get('selectedCat')
      newVote.author = self.request.get('username')
      if selectedItem == previousitem1:
          newVote.winner = selectedItem
          newVote.loser = previousitem2
          newVote.put()
      elif selectedItem == previousitem2:
          newVote.winner = selectedItem
          newVote.loser = previousitem1
          newVote.put()
      else:
          # Do Nothing
          selectedItem = ""         
      
      if previousComment1 != None: 
          if previousComment1 != "":
              newComment = AllComments()
              newComment.loggedInUser = loggedInUser
              newComment.categoryName = selectedCat
              newComment.itemName = previousitem1
              newComment.itemComment = previousComment1
              newComment.put()
          
      if previousComment2 != None:
          if previousComment2 != "":
              newComment = AllComments()
              newComment.loggedInUser = loggedInUser
              newComment.categoryName = selectedCat
              newComment.itemName = previousitem2
              newComment.itemComment = previousComment2
              newComment.put()
              
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, username)
      count = itemsForUser.count()
      error_msg = ""
      if count < 2:
          error_msg = "Y"
      elif count == 2:
          i = 1
          j = 2
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
        'vote_cast': "Y",
        'loggedInUser': loggedInUser,
        'selectedItem': selectedItem,
        'item1': item1,
        'item2': item2,
        'previousComment1': newComment1,
        'previousComment2': newComment2,
        'selectedCat': selectedCat,
        'author': username
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
      self.response.out.write(template.render(path, template_values))     

class ResultsPage(webapp.RequestHandler):  #View Results on a given category
  def post(self):
      categoryName = self.request.get('catName')
      username = self.request.get('username')
      
      itemsofCateg = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", categoryName, username)
      votesofCateg = db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND author = :2", categoryName, username)
      
      for itemCat in itemsofCateg:
          item = itemCat.itemName
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
          newResult.put()
                      
      allResults = db.GqlQuery("SELECT * FROM AllResults WHERE categoryName = :1 AND author = :2 ORDER BY percentWin DESC ", categoryName, username)
      
      template_values = {
        'allResults': allResults,
        'categoryName': categoryName,
        'author': username
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/ResultsPage.html')
      self.response.out.write(template.render(path, template_values))


class ExportXML(webapp.RequestHandler):  #Export XML For a given Category
  def post(self):
        categoryName = self.request.get('catName')
        username = self.request.get('username')
      
        itemsofCateg = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", categoryName, username)
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('Hii')
        self.response.out.write(username)
        self.response.out.write('Hello')
          
        # Create the minidom document
        doc = Document()
        root = doc.createElement("CATEGORY")
        doc.appendChild(root)
        name = doc.createElement("NAME")
        catName = doc.createTextNode(categoryName)
        name.appendChild(catName)
        root.appendChild(name)
        
        for itemofcateg in itemsofCateg:
            item = itemofcateg.itemName
            
            elem = doc.createElement("ITEM")
            insideElem = doc.createElement("NAME")
            value = doc.createTextNode(item)
            insideElem.appendChild(value)
            elem.appendChild(insideElem)
            root.appendChild(elem)
        
        template_values = {
            'document': doc,
            'categoryName': categoryName
            
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/ExportXMLPage.html')
        self.response.out.write(template.render(path, template_values))    
        #print doc.toprettyxml(indent="  ")
           
# Main Procedure for calling the appropriate class            
application = webapp.WSGIApplication(
                                     [('/', Login),
                                      ('/welcome', Welcome),
                                      ('/initChoice', FirstPage),
                                      ('/randomItems', RandomItems),
                                      ('/allItemsForUser', AllItemsForUser),
                                      ('/newAddedItem', NewAddedItem),
                                      ('/newAddedVote', NewAddedVote),
                                      ('/resultsPage', ResultsPage),
                                      ('/exportXML', ExportXML)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()    