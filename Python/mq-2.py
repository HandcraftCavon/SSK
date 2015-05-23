#!/usr/bin/env python
#-----------------------------------------------------
#
#		This is a program for MQ-2 Gas Sensor Module.
#	It could detect danger gas and smokes.
#
#		This program depend on ADC0832 ADC chip. Follow 
#	the instruction book to connect the module and 
#	ADC0832 to your Raspberry Pi.
#
#-----------------------------------------------------

import RPi.GPIO as GPIO
import ADC0832
import time

smoke = 15		# Set MQ-2 pin
BEEP = 16		# Set buzzer pin

def setup():
	GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
	GPIO.setup(smoke, GPIO.IN)		# Set pins' mode is input
	GPIO.setup(BEEP, GPIO.OUT)		# Set pins' mode is output
	ADC0832.setup()					# Setup ADC0832

def loop():
	while True:
		tmp = ADC0832.getResult(0)			# Get analog value from ADC0832
		smokeVal = GPIO.input(smoke)		# Get digital result from MQ-2
		print tmp							# Print analog value
		print smokeVal						# Print digital value
		if smokeVal == 0:					# Beep when smokeval is 0
			print '    ****************'
			print '    * !! DANGER !! *'
			print '    ****************'
			print ''
				
			GPIO.output(BEEP, GPIO.HIGH)	# (0, means detect danger gas)
			time.sleep(0.25)
			GPIO.output(BEEP, GPIO.LOW)
			time.sleep(0.25)
		else :
			time.sleep(0.5)					# Else delay printing.

def destory():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
