#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#include <wiringPi.h>
#include <ds1302.h>

// Register defines

#define	RTC_SECS	 0
#define	RTC_MINS	 1
#define	RTC_HOURS	 2
#define	RTC_DATE	 3
#define	RTC_MONTH	 4
#define	RTC_DAY		 5
#define	RTC_YEAR	 6
#define	RTC_WP		 7
#define	RTC_TC		 8
#define	RTC_BM		31


static unsigned int masks [] = { 0x7F, 0x7F, 0x3F, 0x3F, 0x1F, 0x07, 0xFF } ;

//bcdToD: dToBCD:

static int bcdToD (unsigned int byte, unsigned int mask)
{
  unsigned int b1, b2 ;
  byte &= mask ;
  b1 = byte & 0x0F ;
  b2 = ((byte >> 4) & 0x0F) * 10 ;
  return b1 + b2 ;
}

static unsigned int dToBcd (unsigned int byte)
{
  return ((byte / 10) << 4) + (byte % 10) ;
}


/*
 * ramTest:
 *	Simple test of the 31 bytes of RAM inside the DS1302 chip
 *********************************************************************************
 */

static int ramTestValues [] =
  { 0x00, 0xFF, 0xAA, 0x55, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x00, 0xF0, 0x0F, -1 } ;

static int ramTest (void)
{
  int addr ;
  int got ;
  int i = 0 ;
  int errors = 0 ;
  int testVal ;

  printf ("DS1302 RAM TEST\n") ;

  testVal = ramTestValues [i] ;

  while (testVal != -1)
  {
    for (addr = 0 ; addr < 31 ; ++addr)
      ds1302ramWrite (addr, testVal) ;

    for (addr = 0 ; addr < 31 ; ++addr)
      if ((got = ds1302ramRead (addr)) != testVal)
      {
	printf ("DS1302 RAM Failure: Address: %2d, Expected: 0x%02X, Got: 0x%02X\n",
		addr, testVal, got) ;
	++errors ;
      }
    testVal = ramTestValues [++i] ;
  }

  for (addr = 0 ; addr < 31 ; ++addr)
    ds1302ramWrite (addr, addr) ;

  for (addr = 0 ; addr < 31 ; ++addr)
    if ((got = ds1302ramRead (addr)) != addr)
    {
      printf ("DS1302 RAM Failure: Address: %2d, Expected: 0x%02X, Got: 0x%02X\n",
	      addr, addr, got) ;
      ++errors ;
    }

  if (errors == 0)
    printf ("-- DS1302 RAM TEST: OK\n") ;
  else
    printf ("-- DS1302 RAM TEST FAILURE. %d errors.\n", errors) ;

  return 0 ;
}

/*
 * setLinuxClock:
 *	Set the Linux clock from the hardware
 *********************************************************************************
 */

static int setLinuxClock (void)
{
  char dateTime [20] ;
  char command [64] ;
  int  clock [8] ;


  printf ("Setting the Linux Clock from the DS1302... ") ; fflush (stdout) ;

  ds1302clockRead (clock) ;

// [MMDDhhmm[[CC]YY][.ss]]

  sprintf (dateTime, "%02d%02d%02d%02d%02d%02d.%02d",
	bcdToD (clock [RTC_MONTH], masks [RTC_MONTH]),
	bcdToD (clock [RTC_DATE],  masks [RTC_DATE]),
	bcdToD (clock [RTC_HOURS], masks [RTC_HOURS]),
	bcdToD (clock [RTC_MINS],  masks [RTC_MINS]),
	20,
	bcdToD (clock [RTC_YEAR],  masks [RTC_YEAR]),
	bcdToD (clock [RTC_SECS],  masks [RTC_SECS])) ;

  sprintf (command, "/bin/date %s", dateTime) ;
  system (command) ;

  return 0 ;
}


/*
 * setDSclock:
 *	Set the DS1302 block from Linux time
 *********************************************************************************
 */

static int setDSclock (void)
{
  unsigned long time;
  unsigned long date;
  int weekday;
  int clock [8] ;

  getchar();
  fflush(stdin);
  printf ("Setting the clock in the DS1302 by hand type... ") ;

  scanf("%ld", &date);
  scanf("%ld", &time);
  scanf("%d", &weekday);

  clock [ 0] = dToBcd (time%100) ;		// seconds
  clock [ 1] = dToBcd (time/100%100) ;	// mins
  clock [ 2] = dToBcd (time/100/100) ;	// hours
  clock [ 3] = dToBcd (date%100) ;		// date
  clock [ 4] = dToBcd (date/100%100) ;	// months
  clock [ 5] = dToBcd (weekday) ;		// weekdays
  clock [ 6] = dToBcd (date/100) ;      // years
  clock [ 7] = 0 ;						// W-Protect off

  ds1302clockWrite (clock) ;

  printf ("OK\n") ;

  return 0 ;
}

int main (int argc, char *argv [])
{
  int i ;
  int clock [8] ;

  wiringPiSetup () ;
  ds1302setup   (0, 1, 2) ;

  if (argc == 2)
  {
    /**/ if (strcmp (argv [1], "-slc") == 0)
      return setLinuxClock () ;
    else if (strcmp (argv [1], "-sbh") == 0)
      return setDSclock () ;
    else if (strcmp (argv [1], "-rtest") == 0)
      return ramTest () ;
    else
    {
      printf ("Usage: ds1302 [-slc | -sdsc | -rtest]\n") ;
      return EXIT_FAILURE ;
    }
  }

  for (i = 0 ;; ++i)
  {
    printf ("%5d:  ", i) ;

    ds1302clockRead (clock) ;
    printf (" %2d:%02d:%02d",
	bcdToD (clock [2], masks [2]), bcdToD (clock [1], masks [1]), bcdToD (clock [0], masks [0])) ;

    printf (" %2d/%02d/%04d",
	bcdToD (clock [3], masks [3]), bcdToD (clock [4], masks [4]), bcdToD (clock [6], masks [6]) + 2000) ;
      
    printf ("\n") ;

    delay (200) ;
  }
 
  return 0 ;
}
