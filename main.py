import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <html>
    <body>
    <form action="categoryPage.py" method="get">
      Username: <input type="text" name="username"><br>
      <button type="submit" value="Submit">Submit</button>
      <button type="reset" value="Reset">Reset</button>
    </form>
    </body>
    </html>""")

app = webapp.WSGIApplication([('/', MainPage)],
                              debug=True)

def main():
  run_wsgi_app(app)


if __name__ == '__main__':
  main()