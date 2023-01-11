#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "../include/polling.h"
#define MAX_NUM_FUNCTIONS 10
void doEvery(IntervalFunction *functions, ProgramState *state)
{
    // create array to store the time the function was last executed
    clock_t last_t[MAX_NUM_FUNCTIONS];
    for (int i = 0; i < MAX_NUM_FUNCTIONS; i++)
    {
        last_t[i] = clock();
    }
    while (1)
    {
        for (int i = 0; i < MAX_NUM_FUNCTIONS; i++)
        {
            if (((double)(clock() - last_t[i]) / CLOCKS_PER_SEC) < functions[i].interval || functions[i].interval == -1)
            {
                continue;
            }

            if ((functions[i].f)(state))
            {
                return;
            } // if the function returns 1, stop executing
            last_t[i] = clock();
        }
    }
}