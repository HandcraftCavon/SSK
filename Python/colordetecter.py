#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

OUT = 11
LED = 12
S0 = 13
S1 = 15
S2 = 16
S3 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUT, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(S0,  GPIO.OUT)
GPIO.setup(S1,  GPIO.OUT)
GPIO.setup(S2,  GPIO.OUT)
GPIO.setup(S3,  GPIO.OUT)

cf = [0, 0, 0]

def setup():
	GPIO.output(S0, 0)
	GPIO.output(S1, 1)
	GPIO.output(LED, 1)

def frequency():
	NUM_CYCLES = 10
	start = time.time()
	for impulse_count in range(NUM_CYCLES):
		GPIO.wait_for_edge(11,GPIO.FALLING)
#		print '1'
	duration = time.time() - start
	freq = NUM_CYCLES / duration
	
	return freq

def WB(s0, s1):
	GPIO.output(S0, s0)
	GPIO.output(S1, s1)

def color():
	print 'begin'
	WB(0, 0)			# Red
	cf[0] = frequency()
	WB(1, 1)			# Green
	cf[1] = frequency()	
	WB(0, 1)			# Blue
	cf[2] = frequency()
	WB(1, 0)

def loop():
	while True:
		color()
		for i in range(0, 3):
			print cf[i]
		time.sleep(1)

def destory():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destory()
