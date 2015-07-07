#!/usr/bin/env python
import PCF8591 as ADC
import time
import math

def setup():
	ADC.setup(0x48)

def loop():
	while True:
		analogVal = ADC.read(0)
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		temp = temp - 273.15
		print 'temperature = ', temp, 'C'
		time.sleep(0.2)

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	
