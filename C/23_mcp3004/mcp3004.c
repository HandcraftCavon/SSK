#include <wiringPi.h>
#include <mcp3004.h>
#include <stdio.h>
//Set mcp3004 pinBase as 100
#define mcp3004PB  100

void main(){
	int tmp;
	wiringPiSetup();
	// Setup pcf8591 on base pin 100, and spi device 0
	mcp3004Setup(mcp3004PB, 0);

	while(1){
		tmp = analogRead(mcp3004PB + 0);
		printf("%d\n", tmp);
		delay(10);
	}
}
