#ifndef PROGRAM_STATE_H
#define PROGRAM_STATE_H
#include <stdio.h>
#include "../include/queue.h"

#define MAX_NUM_FUNCTIONS 10
#define ACCEL_UPDATE_INTERVAL 0.1
#define MAX_FILENAME_LENGTH 50
#define AUTO_SAVE_DURATION 30.0

typedef struct ProgramState
{
    double programStart;
    double gravity;
    double queueInterval;
    Queue *timeQueue;
    Queue *accelQueue;
    FILE *logFile;
    FILE *imuDataFile;
} ProgramState;

/**
 * @brief Struct to hold a function and its interval
 * @param f The function
 * @param interval The interval
 * @return IntervalFunction
 */
typedef struct IntervalFunction
{
    int (*f)(struct ProgramState *);
    double interval;
} IntervalFunction;

/**
 * @brief Builds a ProgramState, use this to initialize the state don't create it from the struct
 * @param queueInterval The interval of the queue
 * @param updateInterval The interval of the update
 * @param threshold The threshold of the queue
 * @return ProgramState
 */
ProgramState *buildState(double queueInterval, double updateInterval, double threshold);
/**
 * @brief Changes the state of the program
 *  This is used to change the queue interval
 * @param state The state to change
 * @param queueInterval The new interval of the queue
 */
void changeState(ProgramState *state, double queueInterval);
/**
 * @brief Initializes the functions array to NULL
 * @param functions The array of IntervalFunctions
 */
void initFunctions(IntervalFunction *functions);
FILE *openFileHelper(char *name, char *extension, int num);
/**
 * @brief Opens a file in the output folder
 * If the file already exists, it will add a number to the end of the file name to avoid overwriting
 * @param name The name of the file
 * @param extension The extension of the file
 * @return FILE
 */
FILE *openFile(char *name, char *extension);

#endif