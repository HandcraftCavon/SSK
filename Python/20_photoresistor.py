#!/usr/bin/env python
import ADC0832
import time

def init():
	ADC0832.setup()

def loop():
	while True:
		res = 210 - ADC0832.getResult(0)
		print 'Current illumination : ', res
		time.sleep(0.2)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
