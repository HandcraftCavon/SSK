#!/usr/bin/env python
#------------------------------------------------------
#
#		This is a program for Rheostat Module.
#
#		This program depend on ADC0832 ADC chip. Follow 
#	the instruction book to connect the module and 
#	ADC0832 to your Raspberry Pi.
#
#------------------------------------------------------
import RPi.GPIO as GPIO
import ADC0832

def setup():
	global tmp1			# Define initial value
	ADC0832.setup()		# Setup ADC0832
	tmp1 = ADC0832.getResult(0)		# Get initial value
	print tmp1						# Print the initial calue

def loop():
	while True:
		global tmp1	
		tmp2 = ADC0832.getResult(0)	# Get current value
		if tmp2 != tmp1:			# Print the value if changed
			print tmp2				
			tmp1 = tmp2				# Replace the initial value

def destory():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
