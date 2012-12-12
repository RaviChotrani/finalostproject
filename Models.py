from google.appengine.ext import db

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
  userList = db.ListProperty(str)
  userComment = db.ListProperty(str)
  
class AllComments(db.Model):
  loggedInUser = db.StringProperty()
  categoryName = db.StringProperty()
  itemName = db.StringProperty()
  itemComment = db.StringProperty()
  
class Loggeduser(db.Model):
  loggedInUser = db.StringProperty()
  