#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <wiringPi.h>

//Used to make system calls
int system(const char *command);

int main(int argc, char **argv)
{

  //###################################################
  // EPICS EXAMPLES
  //###################################################

  printf("Starting test of read pin, turn off/on, write to EPICS.\n");

  int pin = 4;

  //Initializes wiringPi using the Broadcom GPIO pin numbers
  wiringPiSetupGpio(); 
  if (wiringPiSetup() == -1) {
    exit(1);
  }

  //Amount of time to loop (default 100)
	int loops = 1000;

	//Start of Clock
	clock_t begin = clock();

	//Loop through, putting to EPICS
	for (int i = 0; i < loops; ++i) {

    char str[10];

    if (digitalRead(pin)) { //If pin is on
      printf("Pin %d is HIGH\n", pin);
      sprintf(str, "%s", "OPEN");
      digitalWrite(pin, 0); //Turn pin off
    } else { //If pin is off
      printf("Pin %d is LOW\n", pin);
      sprintf(str, "%s", "CLOSED");
      digitalWrite(pin, 1); //Turn pin on
    }

    char num[25] = "caput test:lock ";

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
