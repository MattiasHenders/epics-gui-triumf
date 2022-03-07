#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <wiringPi.h>

int main() {

   printf("Starting test of reading and writing pins.\n");

   int pin = 4;

   //Initializes wiringPi using the Broadcom GPIO pin numbers
   wiringPiSetupGpio();
   if (wiringPiSetup() == -1) {
      exit(1);
   }

   int NUM_LOOPS = 1000;

	//Start of Clock
	clock_t begin = clock();

   for (int i = 0; i < NUM_LOOPS; ++i) {

      if (digitalRead(pin)) { //If pin is on
         printf("Pin %d is HIGH\n", pin);
         digitalWrite(pin, 0); //Turn pin off
      } else { //If pin is off
         printf("Pin %d is LOW\n", pin);
         digitalWrite(pin, 1); //Turn pin on
      }
   }

   //Check time
	clock_t end = clock();
	double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

	//Print the output
	printf("Total time spent was %f sec\n", time_spent);

	return 0;
}