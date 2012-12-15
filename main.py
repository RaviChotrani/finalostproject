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
from NewAddedItem import *
from NewAddedVote import NewAddedVote
from ResultsPage import ResultsPage
from ExportXML import ExportXML
from ImportXML import ImportXML
from xml.etree.ElementTree import Element, SubElement, tostring, XML, fromstring
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from xml.parsers import expat
from xml.dom.minidom import parseString
import urllib2
import xml.dom.minidom
import re
  
# Use this for Unit Testing
      #self.response.headers['Content-Type'] = 'text/html'
      #self.response.out.write('Hii')
      #self.response.out.write(selectedCat)
      #self.response.out.write(username)
      #self.response.out.write('Hello')

class Login(webapp.RequestHandler):
  def get(self):
    
    q6 = db.GqlQuery("SELECT * FROM Loggeduser")
    results6 = q6.fetch(100)
    db.delete(results6)  
    
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'  
      template_values = {
          'loggedInUser': users.get_current_user(),
          'url': url,
          'url_linktext': url_linktext 
      }
      path = os.path.join(os.path.dirname(__file__), 'templates/Proceed.html')
      self.response.out.write(template.render(path, template_values))
      
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'
   
      template_values = {
        'url': url,
        'url_linktext': url_linktext
      }
    
      path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
      self.response.out.write(template.render(path, template_values))

class Welcome(webapp.RequestHandler):
  def post(self):
      loggedInUser = self.request.get('loggedInUser')
      logout = self.request.get('logout')
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
      q7 = db.GqlQuery("SELECT * FROM ExpirationTime")
      results7 = q7.fetch(100)
      db.delete(results7)
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
      loggeduser.logout = logout
      loggeduser.put()
      
      template_values = {
        'loggedInUser': loggedInUser,
        'logout': logout
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
      self.response.out.write(template.render(path, template_values))

class WelcomeBack(webapp.RequestHandler):
  def get(self):
      q4 = db.GqlQuery("SELECT * FROM AllResults")
      results4 = q4.fetch(1000)
      db.delete(results4)
          
      loggedInUser = ""
      loggeduser = db.GqlQuery("SELECT * FROM Loggeduser")
      for user in loggeduser:
          loggedInUser = user.loggedInUser
          logout = user.logout
      
      template_values = {
        'loggedInUser': loggedInUser,
        'logout': logout
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
                                      ('/exportXML', ExportXML),
                                      ('/importXML',ImportXML)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()    