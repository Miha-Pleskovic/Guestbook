from google.appengine.ext import ndb

class Guestbook(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
