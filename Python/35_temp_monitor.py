import RPi.GPIO  as  GPIO
import ADC0832   as  ADC
import time
import sys

# BOARD pin numbering
LedR   = 15
LedG   = 16
LedB   = 18
Beep   = 24
JoyBtn = 22

ds18b20 = '28-031467805fff'
location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

def setup():
	global lowl, highl
	lowl = 29
	highl = 31
	ADC.setup()
	GPIO.setup(LedR, GPIO.OUT)
	GPIO.setup(LedG, GPIO.OUT)
	GPIO.setup(LedB, GPIO.OUT)
	GPIO.setup(Beep, GPIO.OUT)
	GPIO.setup(JoyBtn, GPIO.IN)

def beepCtrl(t):
	GPIO.output(Beep, 1)
	time.sleep(t)
	GPIO.output(Beep, 0)
	time.sleep(t)

def tempRead():
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def ledOn(led):
	GPIO.output(LedR, 1)
	GPIO.output(LedG, 1)
	GPIO.output(LedB, 1)
	if led != 0:
		GPIO.output(led,  0)

def joystick():
	global lowl, highl
	if GPIO.input(JoyBtn) == 0:
		destroy()
		quit()
	tempx = ADC.read(0)
	tempy = ADC.read(1)
	if tempx <= 10 and lowl < highl-1:
		lowl += 1
	if tempx >= 245:
		lowl -= 1
	if tempy <= 10:
		highl += 1
	if tempy >= 245 and lowl < highl-1:
		highl -= 1

def loop():
	while True:
		joystick()
		temp = tempRead()
		print 'The lower limit of temperature : ', lowl
		print 'The upper limit of temperature : ', highl
		print 'Current temperature : ', temp
		if float(temp) < float(lowl):
			ledOn(LedB)
			for i in range(0, 3):
				beepCtrl(0.5)
		if temp >= float(lowl) and temp < float(highl):
			ledOn(LedG)
		if temp >= float(highl):
			ledOn(LedR)
			for i in range(0, 3):
				beepCtrl(0.1)

def destroy():
	ledOn(0)
	GPIO.output(Beep, 1)
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
