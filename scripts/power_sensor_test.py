#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
 
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
 
vPin = 0
cPin = 1
 
while True:
    vTot = 0
    for i in range(1000):
        vRead =  readadc(vPin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        vTot += vRead
    vRead = vTot / 1000 / 1

    millivolts = vRead * ( 3300.0 / 1024.0)
 
    millivolts = millivolts * 4.57831325301205
    print "%d V ( %d raw V ) ( %d mV )" % ( millivolts + 570, millivolts, millivolts )

    cTot = 0
    for i in range(1000):
        cRead = readadc(cPin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        cTot += cRead
    cRead = cTot / 1000 / 1
    
    cMv = cRead * ( 3300.0 / 1024.0 )
    cCur = 0
    if cMv > 1650:
        cCur = ( cMv - 1650 ) / 185
    else:
        cCur = ( 1650 - cMv ) / 185
    cCur = cCur * 1000
#    cCur = cMv / 185
#    cCur = ( 1000 * ( 0.0252 * ( cRead - 492 ))) - 94
    print "%d mA ( %d mV )" % ( cCur, cMv )

    time.sleep(1)
