import webapp2


class MainPage(webapp2.RequestHandler):
    print "SI"
    def get(self):
        callback = self.request.get('callback')

        if callback:
          self.response.headers['Content-Type'] = 'application/javascript'
          self.response.out.write(callback + "(" + str(self.request.headers) + ")")
        else:
          self.response.headers['Content-Type'] = 'application/json'
          self.response.out.write(str(self.request.headers))


app = webapp2.WSGIApplication([
    ('/learn', MainPage),
], debug=False)
