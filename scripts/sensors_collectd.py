import RPi.GPIO as GPIO
import time

if __name__ != '__main__':
    GPIO.setwarnings(False)
    import collectd

GPIO.setmode(GPIO.BCM)

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# how many times to read for averaging
readReps = 1000

#pin definitions!
intTempPin = 5
intLightPin = 1

extTempPin = 4
extLightPin = 0

currentPin = 6
voltagePin = 7

battPinA = 2
battPinB = 3

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:   
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
 
        adcout /= 2       # first bit is 'null' so drop it
        return adcout

def avgRead(pin):
    total = 0
    for i in range(readReps):
        read =  readadc(pin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        total += read
    return total / readReps / 1

def readVoltage():
    vRead = avgRead(voltagePin)
    return ( ( vRead * ( 3300.0 / 1024 ) ) * 4.57831325301205 ) + 200

def readCurrent():
    cRead = avgRead(currentPin)
    cMv = cRead * ( 3300.0 / 1024.0 )
    cCur = 0
    
    if cMv > 1650:
        cCur = ( cMv - 1650 ) / 185
    else:
        cCur = ( 1650 - cMv ) / 185

    return cCur * 1000

def readTemp(pin):
    tRead = avgRead(pin)
    mv = tRead * ( 3300.0 / 1024.0 )
    tempC = ( ( mv - 100.0 ) / 10.0) - 40.0
    tempF = ( tempC * 9.0 / 5.0 ) + 32
    return tempF

def readLight(pin):
    return avgRead(pin)

class PiSensors(object):
    def __init__(self):
        self.plugin_name = "pi_sensors"

    def submit(self, instance, value):
        v = collectd.Values()
        v.plugin = self.plugin_name
        v.type = 'gauge'
        v.plugin_instance = 'pi'
        v.type_instance = instance
        v.values = [value,]
        v.dispatch()

    def do_sensors(self):
        self.submit('mv', readVoltage())
        self.submit('ma', readCurrent())
        self.submit('temp_ext', readTemp(extTempPin))
        self.submit('light_ext', readLight(extLightPin))
        self.submit('temp_int', readTemp(intTempPin))
        self.submit('light_int', readLight(intLightPin))
        self.submit('temp_batt_a', readTemp(battPinA))
        self.submit('temp_batt_b', readTemp(battPinB))
    
if __name__ == '__main__':
    print "A Test Mode For You"
    while True:
        print "%d mv %d ma" % ( readVoltage(), readCurrent() )
        print "%d F %d l (ext)" % ( readTemp(extTempPin), readLight(extLightPin) )
        print "%d F %d l (int)" % ( readTemp(intTempPin), readLight(intLightPin) )
        print "%d F %d F (batt)" % ( readTemp(battPinA), readTemp(battPinB) )
        time.sleep(2)
else:
    pisensors = PiSensors()
    collectd.register_read(pisensors.do_sensors)
