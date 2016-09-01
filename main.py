#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import jinja2
import webapp2
import sys
from models import Guestbook

reload(sys)
sys.setdefaultencoding("utf8")

template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class ResultHandler(BaseHandler):
    def post(self):
        error = False
        name = self.request.get("name") or "Neznanec"
        email = self.request.get("email") or "Neznanec"
        message = self.request.get("message")

        entire_data = name + email + message

        for letter in entire_data:
            if letter == "<" or letter == ">" or letter == "/":
                self.write("V besedilu so bili zaznani nedovoljeni znaki. Prosimo, poskusite znova.")
                error = True
                break

        if error == False:
            saved_message = Guestbook(name=name, email=email, message=message)
            saved_message.put()
            return self.redirect_to("seznam-sporocil")

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        list = Guestbook.query(Guestbook.deleted == False).fetch()
        params = {"seznam": list}
        return self.render_template("seznam_sporocil.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("posamezno_sporocilo.html", params=params)

class UrediSporociloHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, message_id):
        msg = self.request.get("message")
        message = Guestbook.get_by_id(int(message_id))
        message.message = msg
        message.put()
        return self.redirect_to("seznam-sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        message.deleted = True
        message.put()
        return self.redirect_to("seznam-sporocil")

class SeznamIzbrisanihSporocilHandler(BaseHandler):
    def get(self):
        list = Guestbook.query(Guestbook.deleted == True).fetch()
        params = {"seznam": list}
        return self.render_template("seznam_izbrisanih_sporocil.html", params=params)

class ObnoviIzbrisanoSporociloHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("obnovi_sporocilo.html", params=params)

    def post(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        message.deleted = False
        message.put()
        return self.redirect_to("seznam-izbrisanih-sporocil")

class TrajniIzbrisHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("trajno_izbrisi_sporocilo.html", params=params)

    def post(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        message.key.delete()
        return self.redirect_to("seznam-izbrisanih-sporocil")


app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler),
    webapp2.Route("/rezultat", ResultHandler),
    webapp2.Route("/seznam-sporocil", SeznamSporocilHandler, name="seznam-sporocil"),
    webapp2.Route("/sporocilo/<message_id:\d+>", PosameznoSporociloHandler),
    webapp2.Route("/sporocilo/<message_id:\d+>/uredi", UrediSporociloHandler),
    webapp2.Route("/sporocilo/<message_id:\d+>/izbrisi", IzbrisiSporociloHandler),
    webapp2.Route("/seznam-izbrisanih-sporocil", SeznamIzbrisanihSporocilHandler, name="seznam-izbrisanih-sporocil"),
    webapp2.Route("/sporocilo/<message_id:\d+>/obnovi", ObnoviIzbrisanoSporociloHandler),
    webapp2.Route("/sporocilo/<message_id:\d+>/trajni-izbris", TrajniIzbrisHandler),
], debug=True)
