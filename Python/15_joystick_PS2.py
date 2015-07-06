#!/usr/bin/env python
#------------------------------------------------------
#
#		This is a program for JoystickPS2 Module.
#
#		This program depend on PCF8591 ADC chip. Follow 
#	the instruction book to connect the module and 
#	ADC0832 to your Raspberry Pi.
#
#------------------------------------------------------
import PCF8591 as ADC 
import RPi.GPIO as GPIO
import time

def setup():
	ADC.Setup(0x48)					# Setup PCF8591
	global state
	state = ['home', 'up', 'down', 'left', 'right', 'pressed', 'release']	

def direction():	#get joystick result
	if ADC.read(0) == 0:
		return 1		#up
	if ADC.read(0) == 255:
		return 2		#down

	if ADC.read(1) == 255:
		return 3		#left
	if ADC.read(1) == 0:
		return 4		#right

	if ADC.read(2) == 0:
		return 5		# Button pressed

	if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15	and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
		return 0

def loop():
	status = 0
	while True:
		tmp = direction()
		if tmp != None and tmp != status:
			print state[tmp]
			status = tmp

def destory():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
