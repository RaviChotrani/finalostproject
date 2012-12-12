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
from FirstPage import FirstPage
from RandomItems import RandomItems
from AllItemsForUser import AllItemsForUser
from NewAddedItem import NewAddedItem
from NewAddedVote import NewAddedVote
from ResultsPage import ResultsPage
from ExportXML import ExportXML
  
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
      
      #Small utility to clear records -- Uncomment only to clear records and then comment back
      '''
      q1 = db.GqlQuery("SELECT * FROM AllCategories")
      results1 = q1.fetch(100)
      db.delete(results1)
      q2 = db.GqlQuery("SELECT * FROM AllItems")
      results2 = q2.fetch(100)
      db.delete(results2)
      q3 = db.GqlQuery("SELECT * FROM AllVotes")
      results3 = q3.fetch(100)
      db.delete(results3)
      q5 = db.GqlQuery("SELECT * FROM AllComments")
      results5 = q5.fetch(100)
      db.delete(results5)
      '''
      
      # Deleting all Records of AllResults to avoid multiple record entries
      q4 = db.GqlQuery("SELECT * FROM AllResults")
      results4 = q4.fetch(1000)
      db.delete(results4)
      
      q6 = db.GqlQuery("SELECT * FROM Loggeduser")
      results6 = q6.fetch(100)
      db.delete(results6)
      
      loggeduser = Loggeduser()
      loggeduser.loggedInUser = loggedInUser
      loggeduser.put()
      
      template_values = {
        'loggedInUser': loggedInUser,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
      self.response.out.write(template.render(path, template_values))

class WelcomeBack(webapp.RequestHandler):
  def get(self):
      
      loggedInUser = ""
      loggeduser = db.GqlQuery("SELECT * FROM Loggeduser")
      for user in loggeduser:
          loggedInUser = user.loggedInUser
          
      template_values = {
        'loggedInUser': loggedInUser,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
      self.response.out.write(template.render(path, template_values))

# Main Procedure for calling the appropriate class            
application = webapp.WSGIApplication(
                                     [('/', Login),
                                      ('/welcome', Welcome),
                                      ('/welcomeBack', WelcomeBack),
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