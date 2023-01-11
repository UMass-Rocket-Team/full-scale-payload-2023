#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "../include/accel.h"
#include "../include/queue.h"
#include "../include/polling.h"

double randInRange(double low, double high)
{
    return ((double)rand() * (high - low)) / (double)RAND_MAX + low;
}
double *makeAccel(int isHigh)
{
    double *output = malloc(sizeof *output * 3);
    if (isHigh)
    {
        output[0] = randInRange(0, 0.5);
        output[1] = randInRange(0, 0.5);
        output[2] = randInRange(10, 17);
    }
    else
    {
        output[0] = randInRange(0, 0.05);
        output[1] = randInRange(0, 0.05);
        output[2] = randInRange(9.7, 10.05);
    }

    return output;
}


int dataUpdater(ProgramState *state)
{
    double curTime = CUR_TIME_DOUBLE;
    double *accel = (!(curTime > 5 && curTime < 25)) ? makeAccel(1) : makeAccel(0);
    double accelMagnitude = sqrt(accel[0] * accel[0] + accel[1] * accel[1] + accel[2] * accel[2]);
    free(accel);
    if (enqueue(state->accelQueue, accelMagnitude) || enqueue(state->timeQueue, CUR_TIME_DOUBLE))
    {
        return 1;
    }
    while (state->timeQueue->size > 0 && ((CUR_TIME_DOUBLE - front(state->timeQueue)) > state->queueInterval))
    {
        dequeue(state->timeQueue);
        dequeue(state->accelQueue);
    }
    return 0;
}

void printAccel(double *accel)
{
    for (int i = 0; i < 3; i++)
    {
        printf("%f\t", accel[i]);
    }
    printf("\n");
}