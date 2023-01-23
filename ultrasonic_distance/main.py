from sensor import pres_sensor
import time
    
presence_sensor = pres_sensor(2,4)

while(1):
    try:
        print(presence_sensor.getPresence())
        time.sleep(1)
    except OSError as ex:
        print(ex.args[0])
        time.sleep(1)