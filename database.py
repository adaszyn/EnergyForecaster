import settings
import mysql.connector

class Database(object):
	def __init__(self):
		super(Database, self).__init__()
		self.config = {
  			'user': settings.DB_USERNAME,
  			'password': settings.DB_PASSWORD,
  			'host': settings.DB_HOST,
  			'port':  settings.DB_PORT,
  			'database': settings.DB_DATABASE,
  			'raise_on_warnings': True,
		}
	def connect(self):
		try:
			self.connection = mysql.connector.connect(**self.config)
		except:
			# to be implemented
			pass 
		print 'database connection - ok.'
	def close_connection(self):
		try:
			self.connection.close()
		except:
			# to be implemented
			pass
		print 'database connection closed.'
