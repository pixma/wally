#
# Author: Annim Banerjee
#

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import pymongo
from datetime import datetime
import hashlib
import sys



class SignUpHandler( tornado.web.RequestHandler ):
	def get(self):
		self.render('signup.html', title='Wally : Sign Up')
		
	def post(self):
		try:
			userName = self.get_argument( "email" )
			password = self.get_argument( "password" )
			firstName = self.get_argument( "firstName" )
			lastName = self.get_argument( "lastName" )
			conn = pymongo.Connection()
			db = conn.wally
			collection = db.userCollection
			## check it email already exist or not
			## if not exist then proceed.
			hashOutput = hashlib.md5( userName.encode() )
			ownerId = hashOutput.hexdigest()
			document = {"entrytype" : "signUp",
						"author" : userName,
						"userName": userName,
						"passwd": password,
						"firstName" : firstName,
						"lastName" : lastName,
						"OwnerID" : ownerId,
						"TS" : datetime.utcnow()}
			objectId = collection.insert( document )
			conn.close()
			self.write({"success":True})#response
			#completion of insertion and creation of new user.
		except:
			print "Unexpected error: ", sys.exc_info()

class SignInHandler( tornado.web.RequestHandler ):
	def get(self):
		self.write( "<head> <script>window.location.replace(\"/\"); </script> </head>" );
	
	def post(self):
		user = self.get_argument( "email" )
		passwd = self.get_argument( "password" )
		conn = pymongo.Connection()
		db = conn.wally
		collection = db.userCollection
		
		if( collection.find({'userName':user,'passwd':passwd}).count() != 1 ):
			self.write( { "LogIn":False } )
			conn.close()
			return

		collection = db.userActivity
		document = {
					"entrytype":"userActivity",
					"status":"Online",
					"userName":user,
					"TS":datetime.utcnow()}
		objId = collection.insert( document )
		conn.close()
		self.write({"LogIn":True})

class UserDashboardHandler( tornado.web.RequestHandler ):
	def get(self, userNickName):
		self.render( 'user.html', title = 'Wally : Home', nickName = userNickName )

class DeviceAddHandler( tornado.web.Requesthandler ):
	def post( self ):
		ownerName = self.get_argument( "userName" )
		devId = self.get_argument( "devId" )
		devMacAddr = self.get_argument( "devMacAddr" )
		devNickName = self.get_argument( "devNickName" )
		ownerId = self.get_argument( "ownerID" )
		#Now connect to DB and log this into DB.
		conn = pymongo.Connection()
		db = conn.wally
		collection = db.devCollection
		document = {"Owner ID" : ownerId,
					"Device ID" : devId,
					"Device Mac Addr" : devMacAddr,
					"Device Name" : devNickName}
		objIdentity = collection.insert( document )
		#Now this device is Unlocked.
		conn.close()
		self.write( {"DeviceAdded":True} )

class OwnerIdQueryHandler( tornado.web.RequestHandler ):
	def post( self ):		
		conn = pymongo.Collection()
		db = conn.wally
		collection = db.userCollection
		


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
	(r"/static/scripts/(.*)", tornado.web.StaticFileHandler, {"path" : "./public/script"},),
	(r"/ws", WebSocketHandler),
	(r"/signUp/", SignUpHandler),
	(r"/signIn/", SignInHandler),
	(r"/user/dashboard/([^/]+)", UserDashboardHandler),
	(r"/deviceAddPoint/", DeviceAddHandler),
	(r"/ownerIdOf/", OwnerIdQueryHandler),
], debug=True, template_path='views')

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(80)
	tornado.ioloop.IOLoop.instance().start()
	
	