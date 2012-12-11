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

class ExportXML(webapp.RequestHandler):  #Export XML For a given Category
  def post(self):
        loggedInUser = self.request.get('loggedInUser')
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
            'categoryName': categoryName,
            'loggedInUser': loggedInUser
            
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/ExportXMLPage.html')
        self.response.out.write(template.render(path, template_values))    
        #print doc.toprettyxml(indent="  ")
 