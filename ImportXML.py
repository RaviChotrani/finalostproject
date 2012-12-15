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
from xml.etree.ElementTree import Element, SubElement, tostring, XML, fromstring
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from xml.parsers import expat
from xml.dom.minidom import parseString
import urllib2
import xml.dom.minidom
import re

def is_present(self, user_name, category_name):
    categories = db.GqlQuery("SELECT * FROM AllCategories WHERE categoryName = :1 AND author = :2", category_name, user_name)

    for category in categories:
        if category.categoryName == category_name:
            return True

    return False

def createNewItem(item_name, category_name, user_name):
    item_new = AllItems(categoryName=category_name,author=user_name,itemName=item_name)
    item_new.author = user_name
    item_new.categoryName = category_name
    item_new.itemName = item_name
    item_new.put()

def delete_item(item_name, category_name, user_name):
      deleteFromAllItems = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2 AND itemName = :3", 
                             category_name, user_name, item_name)
      results = deleteFromAllItems.fetch(100)
      db.delete(results)
      
      deleteFromAllComments = db.GqlQuery("SELECT * FROM AllComments WHERE categoryName = :1 AND itemName = :2", 
                               category_name, item_name)
      results = deleteFromAllComments.fetch(100)
      db.delete(results)
      
      deleteFromAllWinners =  db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND winner = :2", 
                                category_name, item_name)
      results = deleteFromAllWinners.fetch(100)
      db.delete(results)
          
      deleteFromAllLosers =  db.GqlQuery("SELECT * FROM AllVotes WHERE categoryName = :1 AND loser = :2", 
                               category_name, item_name)
      results = deleteFromAllLosers.fetch(100)
      db.delete(results)
          
class ImportXML(webapp.RequestHandler):  #Import XML
  def post(self):
        loggedInUser = self.request.get('loggedInUser')
        logout = self.request.get('logout')
        x = self.request.POST.multi['imported_file'].file.read()
        # check whether the xml file is a valid one and according to the desired format and tag names
        dom = xml.dom.minidom.parseString(x)

        # parse xml file        
        root = fromstring(x)                        
        categoryName = root.findall('NAME')
        
        categoryName = categoryName[0].text
        #self.response.out.write("<br/>category = " + categoryName)
        
        # check whether the category with the same name is already present
        if is_present(self, loggedInUser, categoryName) == False:
            # create a new category with new name
            category_new = AllCategories(categoryName=categoryName,author=loggedInUser)
            category_new.author = loggedInUser
            category_new.categoryName = categoryName
            category_new.put()

            # add items in the newly created category
            for child in root:
                if child.tag == "ITEM":
                    childName = child.findall('NAME')
                    createNewItem(item_name=childName[0].text, category_name=categoryName, user_name=loggedInUser)
        
        else:
            self.response.out.write('This Category is already present. Updating Item List for the Category.')
            xmlItemList = []
            for child in root:
                if child.tag == "ITEM":
                    childName = child.findall('NAME')
                    xmlItemList.append(childName[0].text)
             
            dbItemList = []
            itemsForUser = db.GqlQuery("SELECT * FROM AllItems WHERE categoryName = :1 AND author = :2", categoryName, loggedInUser)
            for item in itemsForUser:
                dbItemList.append(item.itemName)
                
            is_dbItem_present = "F"    
            for dbItem in dbItemList:
                is_dbItem_present = "F"
                for xmlItem in xmlItemList:    
                    if dbItem == xmlItem:
                        is_dbItem_present = "T"
                        break
                
                if is_dbItem_present == "F":
                    delete_item(item_name=dbItem, category_name=categoryName, user_name=loggedInUser)
            
            is_xmlItem_present = "F"
            for xmlItem in xmlItemList:
                is_xmlItem_present = "F"
                for dbItem in dbItemList:
                    if xmlItem == dbItem:
                        is_xmlItem_present = "T"
                        break
                
                if is_xmlItem_present == "F":
                    createNewItem(item_name=xmlItem, category_name=categoryName, user_name=loggedInUser)
                        
                    
                                 
        template_values = {
          'loggedInUser':loggedInUser,
          'logout': logout,
          'import_success': "Y"                 
        }                           
        
        path = os.path.join(os.path.dirname(__file__), 'templates/ImportXML.html')
        self.response.out.write(template.render(path, template_values))