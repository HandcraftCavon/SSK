#!/usr/bin/env python

import RPi.GPIO as GPIO
import ADC0832
import time

FLAME = 15

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(FLAME, GPIO.IN)
	ADC0832.setup()

def loop():
	while True:
		flameVal = ADC0832.getResult(0)
		print GPIO.input(FLAME)
		if GPIO.input(FLAME) == 0:
			print '*********************'
			print '* !! DETECT FIRE !! *'
			print '*********************'
			print ''
		print flameVal
		time.sleep(0.5)

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
