#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//Used to make system calls
int system(const char *command);

int main(int argc, char **argv) {

	printf("Starting test of make heavy system calls.\n");

	//Amount of time to loop (default 100)
	int loops = 1000;

	//Start of Clock
	clock_t begin = clock();

	//Loop through, putting to EPICS
	for (int i = 0; i < loops; ++i) {

		//Make heavy system call
		system("sleep 0.00001");
	}

	//Check time
	clock_t end = clock();
	double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

	//Print the output
	printf("Total time spent was %f sec\n", time_spent);
}
