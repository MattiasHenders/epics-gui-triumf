#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <cadef.h>
#include <time.h>

int main(int argc, char **argv)
{    

    //###################################################
    // EPICS EXAMPLES
    //###################################################

    chid fred;

    int NUM_LOOPS = 100;

    clock_t begin = clock();

    for (int i = 0; i < NUM_LOOPS; ++i) {
        
        SEVCHK(ca_put(DBR_STRING, fred, "0"), "Put failed");
        ca_flush_io();

        SEVCHK(ca_put(DBR_STRING, fred, "1"), "Put failed");
        ca_flush_io();

    }

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%f\n", time_spent);

  return 0;

} // main
