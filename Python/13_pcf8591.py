#!/usr/bin/env python
import PCF8591 as ADC

def loop():
	while True:
		ADC.write(ADC.read(0))

def destroy():
	ADC.write(0)

if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
