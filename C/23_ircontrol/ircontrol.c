#include <wiringPi.h>
#include <errno.h>
#include <softPwm.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lirc/lirc_client.h>
#include <time.h>

#define uchar unsigned char

//The WiringPi pin numbers used by our LEDs
#define Rpin 0
#define Gpin 1
#define Bpin 2
 
#define ON 1
#define OFF 0

uchar color[3] = {0x00, 0x00, 0x00};
uchar Lv[3]    = {0x00, 0x33, 0xE6};

char *keymap[21] ={
	" KEY_CHANNELDOWN ",
	" KEY_CHANNEL ",
	" KEY_CHANNELUP ",
	" KEY_PREVIOUS ",
	" KEY_NEXT ",
	" KEY_PLAYPAUSE ",
	" KEY_VOLUMEDOWN ",
	" KEY_VOLUMEUP ",
	" KEY_EQUAL ",
	" KEY_NUMERIC_0 ",
	" BTN_0 ",
	" BTN_1 ",
	" KEY_NUMERIC_1 ",
	" KEY_NUMERIC_2 ",
	" KEY_NUMERIC_3 ",
	" KEY_NUMERIC_4 ",
	" KEY_NUMERIC_5 ",
	" KEY_NUMERIC_6 ",
	" KEY_NUMERIC_7 ",
	" KEY_NUMERIC_8 ",
	" KEY_NUMERIC_9 "};

void ledColorSet();

void ledInit(void)
{
    softPwmCreate(Rpin, 0, 100);
    softPwmCreate(Gpin, 0, 100);
    softPwmCreate(Bpin, 0, 100);
	ledColorSet(color);
}

void ledColorSet()
{
	printf("%X\n", color[0]);
    softPwmWrite(Rpin, color[0]);
    softPwmWrite(Gpin, color[1]);
    softPwmWrite(Bpin, color[2]);
}

int key(char *code){
	int i;
	int num;
	for (i=0; i<21; i++){
		if (strstr(code, keymap[i])){
			num = i;
		}
	}
	return num + 1;
}

int RGB(int i){
	switch(i){
		case 1: color[0] = Lv[0]; printf("%d\n", i); break;
		case 2: color[0] = Lv[1]; printf("%d\n", i); break;
		case 3: color[0] = Lv[2]; printf("%d\n", i); break;
		case 4: color[1] = Lv[0]; printf("%d\n", i); break;
		case 5: color[1] = Lv[1]; printf("%d\n", i); break;
		case 6: color[1] = Lv[2]; printf("%d\n", i); break;
		case 7: color[2] = Lv[0]; printf("%d\n", i); break;
		case 8: color[2] = Lv[1]; printf("%d\n", i); break;
		case 9: color[2] = Lv[2]; printf("%d\n", i); break;
	}
}

int main()
{
	ledInit();
	RGB(1);
	RGB(4);
	RGB(7);
	ledColorSet();
}

int loop(void)
{
    struct lirc_config *config;
 
    //Timer for our buttons
    int buttonTimer = millis();
 
    char *code;
    char *c;

    ledInit();

    if (wiringPiSetup () == -1)
        exit (1) ;
 
    if(lirc_init("lirc",1)==-1)
        exit(EXIT_FAILURE);
 
    //Read the default LIRC config at /etc/lirc/lircd.conf  This is the config for your remote.
    if(lirc_readconfig(NULL,&config,NULL)==0)
    {
        //Do stuff while LIRC socket is open  0=open  -1=closed.
        while(lirc_nextcode(&code)==0)
        {
            //If code = NULL, meaning nothing was returned from LIRC socket,
            //then skip lines below and start while loop again.
            if(code==NULL) continue;{
                //Make sure there is a 400ms gap before detecting button presses.
                if (millis() - buttonTimer  > 400){
                    //Check to see if the string "KEY_1" appears anywhere within the string 'code'.
					RGB(key(code));
					ledColorSet(color);
                }
            }
            //Need to free up code before the next loop
            free(code);
        }
        //Frees the data structures associated with config.
        lirc_freeconfig(config);
    }
    //lirc_deinit() closes the connection to lircd and does some internal clean-up stuff.
    lirc_deinit();
    exit(EXIT_SUCCESS);
}
