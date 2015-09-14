from database import Database
import pprint
import datetime
import time

class SeasonEntry(object):
	"""docstring for SeasonEntry"""
	def __init__(self):
		super(SeasonEntry, self).__init__()
		self.hourly_consumption = {hour: ([],[]) for hour in range(24)}
		
class Calculator(object):
	def __init__(self, buildings):
		super(Calculator, self).__init__()
		self.db = Database()
		self.buildings = buildings
		self.profiles = {building: {} for building in buildings}
		self.winter = SeasonEntry()
		self.startdate = datetime.date(2014, 2, 26)
	def __enter__(self):
		self.db.connect()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.db.close_connection()

	def load_profiles(self):
		cursor = self.db.connection.cursor()
		complicated_query = """
			select t.POD, t.dt, t.valore, t2.TemperatureC from(
				select POD, adddate(data, 
				interval MOD(orario, 24)HOUR) as dt,valore
				from dss_datimultiorari_riga
				where pod in (select pod from dss_immobili where codice=\'%s\') and data=\'%s\' limit 24
			) as t
			join 
			(select DATE_ADD(
        		DATE_FORMAT(Time, "%%Y-%%m-%%d %%H:00:00"),
        		INTERVAL IF(MINUTE(Time) < 30, 0, 1) HOUR
    		) as dt, TemperatureC
 			from dss_meteo where date(Time)=\'%s\' and idComune=305) as t2
			on t.dt=t2.dt"""
		# query = ("SELECT * FROM dss_creem.dss_profili_pod_lunven where pod in (select pod from dss_immobili where codice=%s)")
		time_delta = datetime.timedelta(days=1)
		for xx in range(200):
			start = time.time()
			self.startdate += time_delta
			date_str = str(self.startdate.year) + '/' + str(self.startdate.month).zfill(2) +'/' + str(self.startdate.day).zfill(2)
			pass
			for building, profile in self.profiles.iteritems():
				# print complicated_query % ('2014-09-08', building)
				cursor.execute(complicated_query % (building, date_str, date_str))
				for idx, row in enumerate(cursor):
					# print idx, row
					self.winter.hourly_consumption[idx][0].append(row[2])
					self.winter.hourly_consumption[idx][1].append(row[3])
			end = time.time()
			print date_str + '\t' + str(end - start)
			# pprint.pprint(self.profiles)
		# print self.winter.hourly_consumption