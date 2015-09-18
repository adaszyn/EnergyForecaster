import settings
import csv
from fancyprinter import FancyPrinter
class Writer(object):
	"""interface for Saving objects"""
	def save_season(self, season):
		pass
	def delete_row():
		pass
		
class DbWriter(Writer):
	"""Object responsible for saving rows into db"""
	def __init__(self, connection):
		super(DbWriter, self).__init__()
		self.connection = connection
		self.cursor = connection.cursor()

	def save_season(self, season):
		instert_query = "INSERT INTO dss_predicto_lunven(codice, ora, stagione, slope, intercept) VALUES (\'%s\', %d,%d,%s, %s)"
		self.cursor.execute(instert_query % (building, hour, day_type, str(slope), str(intercept)))
	
class FileWriter(Writer):
	"""Simple file logger with save_row implementation"""
	def __init__(self):
		super(FileWriter, self).__init__()

	def save_season(self, season):
		for type_of_day, values in season.coefficients.iteritems():
			try:
				file_name = settings.OUTPUT_DIR + '/' + season.building + '_' + season.name + '_' + type_of_day
				file_handle = open(file_name, 'w')
				writer = csv.writer(file_handle)
				writer.writerow(('hour', 'slope_heating', 'intercept_heating', 'slope_cooling', 'intercept_cooling'))
				for hour, coefs in values.iteritems():
					writer.writerow((hour, coefs['heating']['slope'], coefs['heating']['intercept'], coefs['cooling']['slope'], coefs['cooling']['intercept']))
			except IOError:
				FancyPrinter().error('No such directory for saving files!')
				return
				
			file_handle.close()
  #   spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
  #   spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
		# except IOError:
		# 	print utils.bcolors.FAIL + 'directory not found!' + utils.bcolors.ENDC
		# 	return
		
		# 