#!/usr/bin/env python
import RPi.GPIO as GPIO

MPin = 11
Gpin   = 12
Rpin   = 13

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
	GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
	GPIO.setup(MPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

def Led(x):
	if x == 0:
		print 'Red'
		GPIO.output(Rpin, 1)
		GPIO.output(Gpin, 0)
	if x == 1:
		print 'Green'
		GPIO.output(Rpin, 0)
		GPIO.output(Gpin, 1)

def loop():
	while True:
		Led(GPIO.input(MPin))


def destroy():
	GPIO.output(Gpin, GPIO.HIGH)       # Green led off
	GPIO.output(Rpin, GPIO.HIGH)       # Red led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

