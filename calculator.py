from database import Database
import datetime
import time
import json
from scipy import stats
import numpy as np
from settings import INTERNAL_TEMP, OUTPUT_DIR, OUTPUT_TYPE 
import utils
from writer import FileWriter, DbWriter
from fancyprinter import FancyPrinter

# from exceptions import NoWriterException

class CurveCalculator(object):
	"""docstring for CurveCalculator"""
	def __init__(self):
		super(CurveCalculator, self).__init__()
	def calculate_coefficients(x_values, y_values):
		slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)		

class SeasonEntry(object):
	"""docstring for SeasonEntry"""
	def __init__(self, name, building, begin, end):
		super(SeasonEntry, self).__init__()
		self.begin = begin
		self.end = end
		self.name = name
		self.building = building
		if begin > end:
			self.season_months = set(range(begin, 13)) | set(range(1, end + 1))
		else:
			self.season_months = set(range(begin, end + 1))
		self.data = {}
		self.coefficients = {
			'working': {},
			'saturdays': {},
			'festivals': {},
		}
	def get_needed_data(self, consumptions, temperatures, profiles):
		working_day_dataset = {idx: ([], []) for idx in range(0,24)}
		saturday_dataset = {idx: ([], []) for idx in range(0,24)}
		sunday_dataset = {idx: ([], []) for idx in range(0,24)}
		for date in consumptions.keys():
			if date.month in self.season_months:
				weekday = date.weekday()
				profile_type = ('working' if weekday < 5 else ('saturdays' if weekday == 5 else 'festivals'))
				current_dataset = (working_day_dataset if weekday < 5 else (saturday_dataset if weekday == 5 else sunday_dataset))
				for hour, cons_measurement in consumptions[date].iteritems():
					try:
						temp_measurement = temperatures[date][hour]
						current_dataset[hour][0].append(cons_measurement - profiles[profile_type][hour])
						current_dataset[hour][1].append(abs(INTERNAL_TEMP - temp_measurement))
					except KeyError:
						pass
		self.data['working'] = working_day_dataset
		self.data['saturdays'] = saturday_dataset
		self.data['festivals'] = sunday_dataset
	def calculate_coefficients(self):
		for type_of_day, dict in self.coefficients.iteritems():
			for hour, value in self.data[type_of_day].iteritems():
				slope, intercept, r_value, p_value, std_err = stats.linregress(value[0], value[1])
				self.coefficients[type_of_day][hour] = {
					'slope': slope, 
					'intercept': intercept 
				}

class Calculator(object):
	def __init__(self, buildings):
		super(Calculator, self).__init__()
		self.db = Database()
		
		self.buildings = buildings
		self.profiles = {building: {'working':{}, 'saturdays': {}, 'festivals': {}} for building in buildings}
		self.startdate = datetime.date(2014, 2, 26)
	def __enter__(self):
		self.db.connect()
		self.cursor = self.db.connection.cursor()
		if OUTPUT_TYPE == 'FILE':
			self.writer = FileWriter()
		elif OUTPUT_TYPE == 'DB':
			self.writer = DbWriter(self.connection)
		else:
			raise IOError()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.db.close_connection()

	def get_consumption_object(self, tuples):
		result = {}
		for tuple in tuples:
			result[tuple[1]] = {(idx+1) % 24: float(measurement) for idx, measurement in enumerate(tuple[3:])}
		return result
	def get_temperature_object(self, tuples):
		result = {}
		for tuple in tuples:
			date = tuple[2].date()
			time = tuple[2].time()
			if date in result:
				result[date][time.hour] = float(tuple[3])
			else:
				result[date] = {time.hour: float(tuple[3])}
		return result
	def get_profile_object(self, list):
		result = {}
		for idx, value in enumerate(list[0][1:]):
			result[(idx+1) %24] = float(value)
		return result

	def load_data(self):
		working_profile_query = "SELECT * FROM dss_creem.dss_profili_pod_lunven where pod in (%s);"
		saturdays_profile_query = "SELECT * FROM dss_creem.dss_profili_pod_sabato where pod in (%s);"
		festivals_profile_query = "SELECT * FROM dss_creem.dss_profili_pod_festivi where pod in (%s);"
		pods_query = "SELECT pod from dss_immobili WHERE codice=\'%s\'"
		consumption_query = "SELECT * FROM dss_creem.dss_datimultiorari where pod in (%s) and year(data) < 2014"
		temperature_query = "SELECT * from dss_meteo where IdComune=%d and year(Time) < 2014"
		comune_query = "SELECT IdComune from dss_immobili where codice='%s'"

		for building in self.buildings:
			print 'loading data for\t%s' % building
			self.cursor.execute(comune_query % building)
			self.comune = self.cursor.fetchone()[0]
			self.comune = 305 # bug in database - to be removed 

			self.cursor.execute(pods_query % building)
			pods = [str(pod[0]) for pod in self.cursor]
			pods_string = (',').join(['"' + pod + '"' for pod in pods])
			
			self.cursor.execute(consumption_query % pods_string)
			consumptions = self.get_consumption_object([el for el in self.cursor])
			
			self.cursor.execute(temperature_query % self.comune) # code for region (for temperatures)
			temperatures = self.get_temperature_object([el for el in self.cursor]) 

			self.cursor.execute(working_profile_query % pods_string)
			self.profiles[building]['working'] = self.get_profile_object([el for el in self.cursor])
			
			self.cursor.execute(saturdays_profile_query % pods_string)
			self.profiles[building]['saturdays'] = self.get_profile_object([el for el in self.cursor])
			
			self.cursor.execute(festivals_profile_query % pods_string)
			self.profiles[building]['festivals'] = self.get_profile_object([el for el in self.cursor])
			
			self.create_seasons(building, consumptions, temperatures, self.profiles[building])
	def create_seasons(self, building, consumptions, temperatures, profile):
		print 'calculating and saving data for\t%s' % building
		se_w = SeasonEntry('winter', building, utils.months.JANUARY, utils.months.MAY)
		se_s = SeasonEntry('summer', building, utils.months.JUNE, utils.months.SEPTEMBER)
		se_w.get_needed_data(consumptions, temperatures, profile)
		se_w.calculate_coefficients()
		self.writer.save_season(se_w)
		se_s.get_needed_data(consumptions, temperatures, profile)
		se_s.calculate_coefficients()
		self.writer.save_season(se_s)
			# csv_work.write(str(key) + ',' + str(slope) + ',' + str(intercept) + '\n')
			
			# slope, intercept, r_value, p_value, std_err = stats.linregress(sat[key][0], sat[key][1])
			# csv_sat.write(str(key) + ',' + str(slope) + ',' + str(intercept) + '\n')
			
			# slope, intercept, r_value, p_value, std_err = stats.linregress(fest[key][0], fest[key][1])
			# csv_fest.write(str(key) + ',' + str(slope) + ',' + str(intercept) + '\n')
	def save_curve_to_db(self,building, hour, day_type, slope, intercept):
		instert_query = "INSERT INTO dss_predicto_lunven(codice, ora, stagione, slope, intercept) VALUES (\'%s\', %d,%d,%s, %s)"
		# print instert_query % (building, hour, day_type, str(slope), str(intercept))
		self.cursor.execute(instert_query % (building, hour, day_type, str(slope), str(intercept))) 

