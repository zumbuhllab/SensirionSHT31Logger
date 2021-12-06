import mysql.connector
import importlib

import config
from error import RecordError

def connect():
	importlib.reload(config)
	return mysql.connector.connect( **config.conf['Logging']['mysql'] )

def record_logs(log_values: list, insert_sensor_ids : bool =False):
	"""
		Records values into the database.
		parameters:
			log_values: list of lists. The format is as follows [['sensor1_name', value1], ['sensor2_name', value2, ['sensor3_name', value3]]
	"""
	try:
		con = connect()
		cursor = con.cursor()
		
		if insert_sensor_ids:
			for row in log_values:
				sql = f"SELECT `sensor_id` FROM `sensors` WHERE `sensor_name`='{row[0]}'"
				cursor.execute(sql)
				results = cursor.fetchall()
				if len(results)==0:
					sql = f"INSERT INTO `sensors` (`sensor_name`, `sensor_friendlyname`) VALUES ('{row[0]}', '{row[0]}')"
					cursor.execute(sql)

		sql = "INSERT INTO `records`(`sensor_id`, `time`, `value`) VALUES "
		for row in log_values:
			sql += "((SELECT `sensor_id` FROM `sensors` WHERE `sensor_name`='{0:s}'), NOW(),{1:f}),".format(row[0], row[1])
		cursor.execute(sql[:-1])
		con.commit()
		cursor.close()
		con.close()
		
	except Exception as x:
		RecordError("Error recording logs into the database. device_name={0} log_values={1} Exception={2}".format(device_name, log_values, x))

if __name__ == "__main__":

	con = mysql.connector.connect( **config.conf['Logging']['mysql'] )
	
	print(con.get_ssl_cipher())
