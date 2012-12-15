import cgi
import os
import random

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import urllib2
from xml.etree.ElementTree import Element, SubElement, tostring, XML, fromstring


from Models import *

class ExportXML(webapp.RequestHandler):  #Export XML For a given Category
  def post(self):
        loggedInUser = self.request.get('loggedInUser')
        catAndUser = self.request.get('catName')
        x = catAndUser.split(',')
        selectedCat = x[0].strip()
        username = x[1].strip()
        username = self.request.get('username')
      
        itemsofCateg = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 ", selectedCat)
        
        self.response.headers['Content-Type'] = 'text/xml'
        
        file_name = selectedCat.replace(' ', '_').replace(',','').replace('@','').replace('.','')
        self.response.headers['Content-Disposition'] = "attachment; filename="+str(file_name)+ ".xml"
        root = Element('CATEGORY')
        categoryName = SubElement(root, 'NAME')
        categoryName.text = categoryName
        for item in itemsofCateg:
            itemTag = SubElement(root, 'ITEM')
            itemNameTag = SubElement(itemTag, 'NAME')
            itemNameTag.text = item.itemName
        self.response.out.write(tostring(root))