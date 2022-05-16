#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <wiringPi.h>

int main() {

   printf("Starting test of reading and writing pins.\n");
   printf("===============================\n");

   int pin = 4;

   //Initializes wiringPi using the Broadcom GPIO pin numbers
   wiringPiSetupGpio();
   if (wiringPiSetup() == -1) {
      exit(1);
   }

   //Number of times to test
   int tests = 1;

   //Amount of time to loop (default 100)
      int loops = 1000;

   //Check if any args
   if(argc == 2) {
		tests = strtol(argv[1], NULL, 10);;
	} else if (argc == 3) {
		tests = strtol(argv[1], NULL, 10);
		loops = strtol(argv[2], NULL, 10);
	}

	printf("Tests: %d | Loops per test: %d\n", tests, loops);
	printf("===============================\n");

   //Total time
   double totalSec = 0.0;

   //Loop through tests
   for (int k = 0; k < tests; ++k) {

      //Start of Clock
      clock_t begin = clock();

      for (int i = 0; i < loops; ++i) {

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
      printf("Time spent was %f sec\n", time_spent);

   }

   if (tests > 1) {
      //Print the final
      printf("===============================\n");
      printf("Total time spent was %f sec\n", totalSec);
      printf("Average spent was %f sec\n", (totalSec/tests));
      printf("===============================\n");
   }

   return 0;

} // main