#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//Used to make system calls
int system(const char *command);

int main(int argc, char **argv) {

	printf("Starting test of make heavy system calls.\n");

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

		//Loop through, putting to EPICS
		for (int i = 0; i < loops; ++i) {

			//Make heavy system call
			system("sleep 0.0001");
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
}
