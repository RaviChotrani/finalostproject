import cgi
import os

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
  itemImage = db.BlobProperty()
  
class AllVotes(db.Model):
  categoryName = db.StringProperty()
  author = db.StringProperty()
  winnerId = db.IntegerProperty()
  loserId = db.IntegerProperty()


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
      #self.response.headers['Content-Type'] = 'text/html'
      #self.response.out.write("Before")
      #self.response.out.write(author)
      #self.response.out.write("After")    

      template_values = {
        'author': author,
        #'categoryAdded' : "N"
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
            'categsForUser': categsForUser
         }

         path = os.path.join(os.path.dirname(__file__), 'templates/UserCategs.html')
         self.response.out.write(template.render(path, template_values))
              
      if initChoice == "opt3":    # Create a new Category
          category = AllCategories()
          self.response.headers['Content-Type'] = 'text/html'
          username = self.request.get('username')
          #self.response.out.write('Hii')
          #self.response.out.write(username)
          #self.response.out.write('Hello')
          category.author = self.request.get('username')
          category.categoryName = self.request.get('catname')
          category.put()
          template_values = {
             'author': username,
             'categoryAdded' : "Y"
          }

          path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
          self.response.out.write(template.render(path, template_values))
          #self.redirect('/welcome')
              
# Main Procedure for calling the appropriate class            
application = webapp.WSGIApplication(
                                     [('/', Login),
                                      ('/welcome', Welcome),
                                      ('/initChoice', FirstPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()    