#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <wiringPi.h>

int main(int argc, char **argv)
{

  //###################################################
  // EPICS EXAMPLES
  //###################################################

  int pin = 4;

  wiringPiSetup(); // Initializes wiringPi using wiringPi's simlified number system.
  wiringPiSetupGpio(); // Initializes wiringPi using the Broadcom GPIO pin numbers

  //Amount of time to loop (default 100)
	int loops = 1000;

	//Start of Clock
	clock_t begin = clock();

	//Loop through, putting to EPICS
	for (int i = 0; i < loops; ++i) {

    char str[10];

    if (digitalRead(17))
      printf("Pin 17 is HIGH\n");
      sprintf(str, "%s", "OPEN");
    else
      printf("Pin 17 is LOW\n");
      sprintf(str, "%s", "CLOSED");

    char num[25] = "caput test:lock ";

    sprintf(str, "%s", "OPEN");
    strcat(num, str);
    system(num);
  }

	//Check time
	clock_t end = clock();
	double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

	//Print the output
	printf("Total time spent was %f sec\n", time_spent);

  return 0;

} // main
