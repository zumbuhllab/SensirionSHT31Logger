#!/usr/bin/python3
import struct, time, db, platform
from config import conf
if __name__ == "__main__":
	db.record_logs([["nonsense", 12], ["nonsense2", 13]], insert_sensor_ids=True)