#/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

HALL_DO = 15

def setup():
	ADC0832.setup()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(HALL_DO, GPIO.IN)

def loop():
	while True:
		res = ADC0832.getResult(0)
		print 'Current intensity of magnetic field : ', 210-res
		if (GPIO.input(HALL_DO) == 0):
			print ''
			print '********************'
			print '* Magnet Approach! *'
			print '********************'
			print ''
		time.sleep(0.2)

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()

