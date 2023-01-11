#ifndef ACCEL_H
#define ACCEL_H
#include "../include/queue.h"
#include "../include/polling.h"
double randInRange(double low, double high);
double *makeAccel(int);
void printAccel(double *accel);
int dataUpdater(ProgramState *state);
#endif