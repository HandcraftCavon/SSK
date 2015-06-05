#!/usr/bin/env python

import time
import LCD1602 as LCD
import PCF8591

LCD.init()

while True:
	for i in range(1, 30):
		LCD.write(10, 0, str(PCF8591.read(0)))
		LCD.write(10, 1, str(PCF8591.read(1)))
	LCD.clear()
	LCD.write(3, 0, 'XVal:')
	LCD.write(3, 1, 'YVal:')

