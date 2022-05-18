#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#include <lgpio.h>

#define LFLAGS 0
#define PIN 23
#define SigOUT 12
#define LOOPS 20000
#define CYCLES 10

int main(int argc, char *argv[]) {
    int h;
    int i;
    int j;
    double t0, t1;
    int status;
    int arr[20000];
    int results[CYCLES];
    int result;
    double sum;
    
   FILE * latencyInformation;
   latencyInformation = fopen ("./c-no-epics/GpioOutC_2022-05-04_CS-BX_x.txt", "w+");
    
    // Runs test for number of cycles
    for (j = 0; j < CYCLES; j++) {
    
      //int result;
      h = lgGpiochipOpen(0);
      
      if (h >= 0) {
        if ((status = lgGpioClaimOutput(h, LFLAGS, SigOUT, 0)) == LG_OKAY) {
          t0 = lguTime();

          for (i = 0; i < LOOPS; ++i) {
            //result = lgGpioRead(h, PIN);
            arr[i] = lgGpioRead(h, PIN);
            //printf("%d", result);
          }

          t1 = lguTime();
          
          FILE *f;
          char name[] = {"./c-no-epics/c_no_epics_x.csv"};
          name[24] = j + '0';
          f = fopen(name, "w+");
          for(i = 0; i < LOOPS; i++) {
            fprintf(f,"%d,\n", arr[i]);
          }
          fclose(f);
          result = (1.0 * LOOPS) / (t1 - t0);
          results[j] = result;
          fprintf(latencyInformation, "lgpio  %d\n", result);
        } else {
          printf("lgGpioClaimSigOUTput FAILED on Pin %d\n", SigOUT);
          lgLineInfo_t lInfo;

          status = lgGpioGetLineInfo(h, SigOUT, &lInfo);

          if (status == LG_OKAY) {
            if (lInfo.lFlags & 1) {
              printf("GPIO in use by the kernel ");
              printf("name=%s  user=%s\n", lInfo.name, lInfo.user);
            }
          }
        }
            lgGpioFree(h, SigOUT);
        lgGpiochipClose(h);
      } else
        printf("Unable to open gpiochip 0\n");
  }
  
  // Calculates the average reads per second
  for (int i = 0; i < CYCLES; ++i) {
    sum += results[i];
  }
  fprintf(latencyInformation, "Average reads per second %0.0f\n", sum/CYCLES);
  fclose(latencyInformation);
}
