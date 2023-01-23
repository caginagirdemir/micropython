import machine,time
from machine import Pin

#### Class function descriptions
# Construction prototype (trig_pin, echo_pin, threshold) 
# Construction defaults (2, 4 ,30(cm))
# getDistance() -> return float as distance in cm SI unit
# checkPin() -> return echo_pin and trig_pin values as string
# getPresence() -> return bool value depend on threshold distance

class pres_sensor:
    __echo_timeout_us = 500*2*30
    __trig_pin = 2
    __echo_pin = 4
    __treshold = 30

    #with argument constructor
    def __init__(self, _trig_pin = 2, _echo_pin = 4, _treshold = 30):
        self.__trig_pin = _trig_pin
        self.__echo_pin = _echo_pin
        self.__treshold = _treshold
        self.trig = Pin(self.__trig_pin, mode=Pin.OUT, pull=None) #Trig Output
        self.trig.value(0) #Set 0V
        self.echo = Pin(self.__echo_pin, mode=Pin.IN, pull=None) #Echo Input

    def set_pulse_and_wait(self):
        self.trig.value(0) #Stabilize the sensor
        time.sleep_us(5)
        self.trig.value(1)
        #send 10us pulse
        time.sleep_us(10)
        self.trig.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.__echo_timeout_us)
        except OSError as ex: 
            if ex.args[0] == 110: # 110 -> TIMEOUT ERROR
                pulse_time = 400
                return pulse_time
                #raise OSError("Out of range")
            raise ex
        if(pulse_time < 0):
            raise OSError("Connection Problem")
        return pulse_time

    def getDistance(self):
        pulse_time = self.set_pulse_and_wait()
        cm = (pulse_time / 2) / 29.1
        return cm

    def getPresence(self):
        val = self.getDistance()
        if(val < self.__treshold):
            return 1
        else:
            return 0


    def checkPin(self):
        retstr = "Trig Pin %d, and Echo Pin %d" % (self.__trig_pin, self.__echo_pin)
        return retstr

# machine.time_pulse_us Prototype (pin, pulse_level, timeout)
# Time a pulse on the given pin, and return the duration of the pulse in microseconds.
# The pulse_level argument should be 0 to time a low pulse or 1 to time a high pulse.
