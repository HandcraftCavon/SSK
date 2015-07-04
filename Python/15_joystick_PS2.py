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

btn = 15	# Define button pin

def setup():
	ADC.Setup(0x48)					# Setup PCF8591
	GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
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

	if ADC.read(0) - 132 < 2 and ADC.read(0) - 132 > -2	and ADC.read(1) - 126 < 2 and ADC.read(1) - 126 > -2 and ADC.read(2) == 255:
		return 0

def loop():
	status = 0
	while True:
		tmp = direction()
		if tmp != None and tmp != status:
#			if status == 5:
#				print state[6]
#			else:
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
