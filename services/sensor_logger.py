import spidev
import time
from data.models import HumidityLog
from data.models import Plant

# SENSORS
SENSOR_fiji_0 = 0 # fiji
SENSOR_1 = 1
SENSOR_2 = 2
SENSOR_3 = 3

# LIST OF SENSORS
SENSORLIST = [
	SENSOR_fiji_0
]

#SPIDEV
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

#VALUES
DRY_VALUE = 1000
WET_VALUE = 400

def read_adc(channel):
	assert 0 <= channel <= 7, "channel must be between 0 and 7"
	
	r = spi.xfer2([1, (8 + channel) << 4, 0])
	value = ((r[1] & 3) << 8) + r[2]
	return value

#convert raw value
def get_humidity_percent(raw_value):
	if raw_value < WET_VALUE:
		return 100
	
	elif raw_value > DRY_VALUE:
		return 0
		
	value = max(min(raw_value, DRY_VALUE), WET_VALUE)
	percent = 100 * (DRY_VALUE - value) / (DRY_VALUE - WET_VALUE)
	return round(percent, 1)

def log_forever():
	print(f"Logging soil moisture from channels {SENSORLIST} every second...")
	
	try:
		while True:
			HumidityLog.delete_old_records()
			for SENSOR in SENSORLIST:
				if not Plant.exists(SENSOR + 1):
					print(f"Skipping sensor {SENSOR}: no plant with that ID.")
					continue

				raw = read_adc(SENSOR)
				humidity = get_humidity_percent(raw)
				HumidityLog.log(SENSOR + 1, humidity)
				
			
			# sleep for one second so all the sensors could provide data
			time.sleep(1)
			
	except KeyboardInterrupt:
		print("Logging stopped by user.")
		spi.close()
