#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//Used to make system calls
int system(const char *command);

int main(int argc, char **argv) {

	printf("Starting test of caputting to EPICS.\n");

	//Number of times to test
	int tests = 1;

	//Amount of time to loop (default 100)
	int loops = 1000;

	//Check if any args
	if(argc == 2) {
		tests = argv[1];
	} else if (argc == 3) {
		tests = argv[1];
		loops = argv[2];
	}

	//Total time
	double totalSec = 0.0;

	printf("Tests: %d | Loops per test: %d\n", tests, loops);
	printf("===============================\n");
	
	//Loop through tests
  	for (int k = 0; k < tests; ++k) {

		//Start of Clock
		clock_t begin = clock();

		//Loop through, putting to EPICS
		for (int i = 0; i < loops; ++i) {

			char num[25] = "caput test:number ";

			char str[4];
			sprintf(str, "%d", i);
			strcat(num, str);
			system(num);
		}

		//Check time
		clock_t end = clock();
		double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    	totalSec += time_spent;

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
}
