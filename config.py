import serial
conf = {
	"ReloadPeriod":		60,
	"PasswordHash":		"xxxxxx",
	"Logging": {
		"SleepInLoop":		1,
		"mysql": {
			"host":			"phys-dots-data.physik.unibas.ch",
			"user":			"logger",
			"password":		"xxxxxxx",
			"database":		"logs"
		}
	},
	"Errorfile":	"/etc/BlueForsMonitor/error.log"
}
