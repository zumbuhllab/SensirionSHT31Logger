#!/usr/bin/python3
import datetime
import importlib

import config

def RecordError(msg):
	importlib.reload(config)
	with open(config.conf["Errorfile"], "a") as f:
		f.writelines(["{0} {1}\n".format(datetime.datetime.now(), msg)])
		print(msg)
