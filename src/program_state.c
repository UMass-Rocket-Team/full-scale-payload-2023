#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "../include/program_state.h"
#include "../include/polling.h"

ProgramState *buildState(double queueInterval, double updateInterval, double threshold)
{
    ProgramState *state = malloc(sizeof *state);
    state->programStart = CUR_TIME_DOUBLE;
    state->gravity = -1;
    state->queueInterval = queueInterval;
    state->timeQueue = createQueue(computeMaxCapacity(updateInterval, queueInterval), -1);
    state->accelQueue = createQueue(computeMaxCapacity(updateInterval, queueInterval), threshold);
    state->logFile = openFile("log", "txt");
    fprintf(state->logFile, "Program Start: %f s\n", state->programStart);
    state->imuDataFile = openFile("imu_data", "csv");
    fprintf(state->imuDataFile, "Time, Temperature, Mag X, Mag Y, Mag Z, Gyro X, Gyro Y, Gyro Z, Acc X, Acc Y, Acc Z, Lin Acc X, Lin Acc Y, Lin Acc Z, Gravity X, Gravity Y, Gravity Z, Euler X, Euler Y, Euler Z\n");
    return state;
}

void changeState(ProgramState *state, double queueInterval)
{
    resetQueue(state->accelQueue);
    resetQueue(state->timeQueue);
    state->queueInterval = queueInterval;
    state->timeQueue = createQueue(computeMaxCapacity(ACCEL_UPDATE_INTERVAL, queueInterval), -1);
    state->accelQueue = createQueue(computeMaxCapacity(ACCEL_UPDATE_INTERVAL, queueInterval), state->gravity);
}

void initFunctions(IntervalFunction *functions)
{
    for (int i = 0; i < MAX_NUM_FUNCTIONS; i++)
    {
        functions[i] = (IntervalFunction){NULL, -1.0};
    }
}
FILE *openFileHelper(char *name, char *extension, int num)
{
    FILE *fptr;
    char path[MAX_FILENAME_LENGTH];
    snprintf(path, MAX_FILENAME_LENGTH, "output/%s%05d.%s", name, num, extension);
    fptr = fopen(path, "r");
    if (fptr == NULL) // if file does not exist, create it
    {
        fptr = fopen(path, "w");
        return fptr;
    }
    else
    {   
        return openFileHelper(name, extension, num+1);
    }
}
FILE *openFile(char *name, char *extension)
{
    return openFileHelper(name, extension, 0);

}

