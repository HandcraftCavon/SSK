#!/usr/bin/env python
import ADC0832 as ADC
import RPi.GPIO as GPIO

b = 0
def loop():
	while True:
		a = ADC.read(0)
		if a < 20:
			print "Voice In!!  ", b
			b += 1

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
