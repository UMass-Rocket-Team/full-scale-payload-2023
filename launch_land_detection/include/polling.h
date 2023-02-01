#ifndef POLLING_H
#define POLLING_H
#include <time.h>
#include "../include/queue.h"
#include "../include/program_state.h"
#define CUR_TIME_DOUBLE ((double)clock() / CLOCKS_PER_SEC)
#define STOP_POLLING 1
#define CONTINUE_POLLING 0
/**
 * @brief Executes functions in the array at their corresponding intervals
 *  See main.c for an example
 * 
 * @param functions The array of IntervalFunctions (see program_state.h)
 * @param state The state of the program (see program_state.h)
 * @return void
 */
void doEvery(IntervalFunction *functions, ProgramState *state);


#endif