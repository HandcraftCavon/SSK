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

color[3] = {0, 0, 0};

void ledInit(void)
{
    softPwmCreate(Rpin, 0, 100);
    softPwmCreate(Gpin, 0, 100);
    softPwmCreate(Bpin, 0, 100);
}

void ledColorSet()
{
    softPwmWrite(Rpin, color[0]);
    softPwmWrite(Gpin, color[1]);
    softPwmWrite(Bpin, color[2]);
}

int main(int argc, char *argv[])
{
    struct lirc_config *config;
 
    //Timer for our buttons
    int buttonTimer = millis();
 
    char *code;
    char *c;

    ledInit();

    if (wiringPiSetup () == -1)
        exit (1) ;
 
    //Initiate LIRC. Exit on failure
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
                    if(strstr (code,"KEY_CHANNELDOWN")){
                        printf("MATCH on KEY_1\n");
                        flipLED(LED1);
                        buttonTimer = millis();
                    }
                    else if(strstr (code,"KEY_CHANNEL")){
                        printf("MATCH on KEY_2\n");
                        flipLED(LED2);
                        buttonTimer = millis();
                    }
                    else if(strstr (code,"KEY_CHANNELUP")){
                        printf("MATCH on KEY_3\n");
                        flipLED(LED3);
                        buttonTimer = millis();
                    }
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
