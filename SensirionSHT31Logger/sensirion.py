#!/usr/bin/python3
import struct, time, db, platform
from config import conf
from error import RecordError

def GetData_Linux():
	import pygatt
	# The BGAPI backend will attempt to auto-discover the serial device name of the
	# attached BGAPI-compatible USB adapter.
	adapter = pygatt.GATTToolBackend()
	# See this manual for information on the Sensirion temperature and humidity sensor:
	# https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Smart-Gadget_User-Guide.pdf

	try:
		humidity = struct.unpack('<f', device.char_read(config["humidity_uuid"], timeout=100))[0]
		temperature = struct.unpack('<f', device.char_read(config["temperature_uuid"], timeout=100))[0]
	except Exception as ex:
		RecordError(f"I have no idea what happened. Try to figure it out for yourself. Here's the error: {ex}")
	return {"temperature": temperature, "humidity": humidity}

def GetData_Windows():
	
	return {"temperature": temperature, "humidity": humidity}




if __name__ == "__main__":
	system = platform.system()
	if system == "Windows":
		import socket
		hostMACAddress = conf['mac_address']
		port=4
		backlog = 1
		size = 1024
		s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
		s.bind((hostMACAddress,port))
		s.listen(backlog)
		try:
			client, address = s.accept()
			while 1:
				data = client.recv(size)
				if data:
					print(data)
					client.send(data)
		except:	
			print("Closing socket")	
			client.close()
			s.close()
		
		exit()
		
	elif system == "Linux":
		try:
			adapter.start()
			device = adapter.connect(mac_address, address_type=pygatt.BLEAddressType.random, timeout=20)
		except Exception as ex:
			RecordError(f"I think I could not connect to the Sensirion sensor through Bluetooth: {ex}")
		finally:
			adapter.stop()
		
	else:
		print("This only words on Windows and Linux. Sorry.")
		exit()
		
	while True:
		if system == "Windows":
			data = GetData_Windows()
		elif system == "Linux":
			data = GetData_Linux()
		try:
			db.record_logs(conf['Machine'],[[conf['Sensors']['humidity'], data["humidity"]],[conf['Sensors']['temperature'], data["temperature"]]])
		except Exception as ex:
			RecordError(f"I have no idea what happened. Try to figure it out for yourself. Here's the error: {ex}")
		
		time.sleep(config.conf["ReloadPeriod"])







