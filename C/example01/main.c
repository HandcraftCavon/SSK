#include "I2CLCD1602.h"
#include <pcf8591.h>
#include <wiringPi.h>

#define PCF 120

void main(){
	init();
	wiringPiSetup();
	clear();
	pcf8591Setup(PCF, 0x48);
	write(4, 0, "Hello");
	write(7, 1, "world!");
	while(1);
}
