#!/usr/bin/python3
import pygatt, struct, time, db, config
from error import RecordError

# See this manual for information on the Sensirion temperature and humidity sensor:
# https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Smart-Gadget_User-Guide.pdf

mac_address = "EA:C2:81:01:06:A5" # This is my sensor's MAC address.
hum_uuid = "00001235-b38d-4985-720e-0f993a68ee41"
tmp_uuid = "00002235-b38d-4985-720e-0f993a68ee41"

# The BGAPI backend will attempt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.GATTToolBackend()

try:
	adapter.start()
	device = adapter.connect(mac_address, address_type=pygatt.BLEAddressType.random, timeout=20)

	while True:
		try:
			humidity = struct.unpack('<f', device.char_read(hum_uuid, timeout=100))[0]
			temperature = struct.unpack('<f', device.char_read(tmp_uuid, timeout=100))[0]

			db.record_logs('BFLD400_Sensirion',[['room_humidity', humidity],['room_temperature', temperature]])
		except Exception as ex:
			RecordError(f"I have no idea what happened. Try to figure it out for yourself. Here's the error: {ex}")

		time.sleep(config.conf["ReloadPeriod"])

except Exception as ex:
	RecordError(f"I think I could not connect to the Sensirion sensor through Bluetooth: {ex}")
finally:
	adapter.stop()

	
