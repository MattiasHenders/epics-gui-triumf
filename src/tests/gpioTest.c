#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define TRUE 1

int main() {

   if (wiringPiSetup () == -1) {
      exit(1);
   }

   pinMode(7, OUTPUT);

   int NUM_LOOPS = 100;

    clock_t begin = clock();

    for (int i = 0; i < NUM_LOOPS; ++i) {

      digitalWrite(7, 0);
      digitalWrite(7, 1);
   }

   clock_t end = clock();
   double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
   printf("%f\n", time_spent);

  return 0 ;
}