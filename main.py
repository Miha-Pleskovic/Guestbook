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
        name = self.request.get("name") or "Neznanec"
        email = self.request.get("email") or "Neznanec"
        message = self.request.get("message")
        saved_message = Guestbook(name=name, email=email, message=message)
        saved_message.put()

        return self.write("Vaše sporočilo je bilo uspešno poslano.")

'''class SeznamSporocilHandler(BaseHandler):
    def get(self):
        list = Guestbook.query().fetch()
        params = {"seznam": list}
        return self.render_template("seznam_sporocil.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, message_id):
        message = Guestbook.get_by_id(int(message_id))
        params = {"sporocilo": message}
        return self.render_template("posamezno_sporocilo.html", params=params)'''

app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler),
    webapp2.Route("/rezultat", ResultHandler),
#    webapp2.Route("/seznam-sporocil", SeznamSporocilHandler),
#    webapp2.Route("/sporocilo/<sporocilo_id:\d+>", PosameznoSporociloHandler)
], debug=True)
