#
# Author: Annim Banerjee
#

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title='Wally : Home')
		
class WebSocketHandler( tornado.websocket.WebSocketHandler ):
	def open(self):
		print "WebSocket Opened"
	
	def on_message(self, message ):
		self.write_message(u"You said: " + message )
		
	def on_close( self ):
		print "socket Closed"

application = tornado.web.Application([
    (r"/", MainHandler),
	(r"/static/styles/(.*)", tornado.web.StaticFileHandler, {"path" : "./public/styles"},),
	(r"/static/images/(.*)", tornado.web.StaticFileHandler, {"path" : "./public/images"},),
	(r"/ws", WebSocketHandler),
], debug=True, template_path='views')

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(80)
	tornado.ioloop.IOLoop.instance().start()
	
	