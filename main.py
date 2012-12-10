import cgi
import os
import random

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
      Username: <input type="text" name="username"><br>
      <button type="submit" value="Login">Submit</button>
      <button type="reset" value="Reset">Reset</button>
    </form>
    </body>
    </html>""")
    
class Welcome(webapp.RequestHandler):
  def post(self):
      author = self.request.get('username')
      # Small utility to clear records -- Uncomment only to clear records and then comment back
      #q = db.GqlQuery("SELECT * FROM AllItems")
      #results = q.fetch(10)
      #db.delete(results)
      
      template_values = {
        'author': author,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
      self.response.out.write(template.render(path, template_values))

class FirstPage(webapp.RequestHandler):
  def post(self):
      initChoice = self.request.get('firstChoice')
      if initChoice == "opt1":    # Vote on Existing Category
          allCategories = db.GqlQuery("SELECT * FROM AllCategories")
          template_values = {
            'allCategories': allCategories
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/AllCategs.html')
          self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt2":    # Edit existing Category 
         username = self.request.get('username')  
         categsForUser = db.GqlQuery("SELECT * FROM AllCategories where author = :1", username)
         
         template_values = {
            'categsForUser': categsForUser,
            'author' : username
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
          #self.redirect('/welcome')

class RandomItems(webapp.RequestHandler):
  def post(self):
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
                 
      template_values = {
        'item1': item1,
        'item2': item2,
        'selectedCat': selectedCat,
        'author': username
        
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
      self.response.out.write(template.render(path, template_values))     
      
      
class AllItemsForUser(webapp.RequestHandler):  # Edit Existing Category : i.e; This supports only addition of items to the category
  def post(self):
      selectedCat = self.request.get('catName')
      username = self.request.get('username')
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", selectedCat, username)
      
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'author': username
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))
      

class NewAddedItem(webapp.RequestHandler):  #To show added item and option to add more
  def post(self):
      selectedCat = self.request.get('catName')
      author = self.request.get('username')
      
      newItem = AllItems()
      newItem.categoryName = self.request.get('catName')
      newItem.author = self.request.get('username')
      newItem.itemName = self.request.get('itemName')
      newItem.put()
      
      itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", 
                                 newItem.categoryName, newItem.author)
      
      template_values = {
        'itemsForUser': itemsForUser,
        'selectedCat': selectedCat,
        'author': author
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/UserItems.html')
      self.response.out.write(template.render(path, template_values))
      
class NewAddedVote(webapp.RequestHandler):  #To update Vote casted and option to vote again on same category
  def post(self):
      selectedCat = self.request.get('selectedCat')
      selectedItem = self.request.get('selectedItem')
      username = self.request.get('username')
      previousitem1 = self.request.get('item1')
      previousitem2 = self.request.get('item2')
      
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
                 
      template_values = {
        'vote_cast': "Y",
        'selectedItem': selectedItem,
        'item1': item1,
        'item2': item2,
        'selectedCat': selectedCat,
        'author': username
        
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/VotePage.html')
      self.response.out.write(template.render(path, template_values))     
                         
# Main Procedure for calling the appropriate class            
application = webapp.WSGIApplication(
                                     [('/', Login),
                                      ('/welcome', Welcome),
                                      ('/initChoice', FirstPage),
                                      ('/randomItems', RandomItems),
                                      ('/allItemsForUser', AllItemsForUser),
                                      ('/newAddedItem', NewAddedItem),
                                      ('/newAddedVote', NewAddedVote)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()    