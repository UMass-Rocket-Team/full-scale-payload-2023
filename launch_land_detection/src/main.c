#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "../include/polling.h"
#include "../include/queue.h"
#include "../include/accel.h"
#include "../include/program_state.h"

#define REFERENCE_GRAVITY_DURATION 10.0

#define MOTOR_BURN_TIME 1.90
#define LAUNCH_PROPORTION_THRESHOLD 0.95
#define LAUNCH_VARIANCE_THRESHOLD 1.5

#define LANDING_DURATION 10.0
#define LANDING_PROPORTION_THRESHOLD 0.05
#define LANDING_VARIANCE_THRESHOLD 0.5

int checkCalibration(ProgramState *state);
int findReferenceGraivty(ProgramState *state);
int checkLaunch(ProgramState *state);
int checkLanding(ProgramState *state);
int autoSaveFiles(ProgramState *state);

int main()
{
    srand(time(0)); // for random acceleration values

    // Initializing program
    ProgramState *state = buildState(REFERENCE_GRAVITY_DURATION, ACCEL_UPDATE_INTERVAL, 9.8);
    IntervalFunction functions[10];
    initFunctions(functions);

    // Calibration
    functions[0] = (IntervalFunction){&checkCalibration, 0.0};
    functions[1] = (IntervalFunction){&autoSaveFiles, AUTO_SAVE_DURATION};
    doEvery(functions, state);

    // Calculate reference gravity
    functions[0] = (IntervalFunction){&dataUpdater, ACCEL_UPDATE_INTERVAL};
    functions[1] = (IntervalFunction){&findReferenceGraivty, REFERENCE_GRAVITY_DURATION * 0.5};
    functions[2] = (IntervalFunction){&autoSaveFiles, AUTO_SAVE_DURATION};
    doEvery(functions, state);

    // Launch Detection
    changeState(state, MOTOR_BURN_TIME * 0.95);
    functions[1] = (IntervalFunction){&checkLaunch, MOTOR_BURN_TIME * 0.25};
    functions[2] = (IntervalFunction){&autoSaveFiles, AUTO_SAVE_DURATION};
    doEvery(functions, state);

    // Landing Detection
    changeState(state, LANDING_DURATION * 0.95);
    functions[1] = (IntervalFunction){&checkLanding, LANDING_DURATION * 0.25};
    functions[2] = (IntervalFunction){&autoSaveFiles, AUTO_SAVE_DURATION};
    doEvery(functions, state);

    // Clean up
    free(state);
    fclose(state->logFile);
    fclose(state->imuDataFile);
    printf("PROGRAM COMPLETE");

    return 0;
}

int checkCalibration(ProgramState *state)
{
    // TODO
    fprintf(state->logFile, "Calibration Complete\n");
    return 1;
}

int findReferenceGraivty(ProgramState *state)
{
    if (CUR_TIME_DOUBLE - front(state->timeQueue) < 0.5 * REFERENCE_GRAVITY_DURATION)
    {
        return 0;
    }
    double *meanAndVariance = getMeanAndVariance(state->accelQueue);
    printf("Mean: %f\tVariance: %f\n", meanAndVariance[0], meanAndVariance[1]);
    if (meanAndVariance[1] < 0.1 && meanAndVariance[0] > 9.6 && meanAndVariance[0] < 10.0)
    {
        state->gravity = meanAndVariance[0] * 1.25;
        printf("Reference Gravity: %f m/s^2\n", state->gravity);
        fprintf(state->logFile, "Reference Gravity: %f m/s^2\n", state->gravity);
        free(meanAndVariance);
        return 1;
    }
    free(meanAndVariance);
    return 0;
}

int checkLaunch(ProgramState *state)
{
    if (CUR_TIME_DOUBLE - front(state->timeQueue) < 0.5 * MOTOR_BURN_TIME)
    {
        return 0;
    }
    double curProportion = getProportionGtThreshold(state->accelQueue);
    printf("Cur Proportion: %f\n", curProportion);
    if (curProportion < LAUNCH_PROPORTION_THRESHOLD)
    {
        return 0;
    }
    double *meanAndVariance = getMeanAndVariance(state->accelQueue);
    printf("Mean: %f\tVariance: %f\n", meanAndVariance[0], meanAndVariance[1]);
    if (meanAndVariance[1] > LAUNCH_VARIANCE_THRESHOLD)
    {
        double launchTime = CUR_TIME_DOUBLE - state->programStart;
        printf("LAUNCH DETECTED: %f s\n", launchTime);
        fprintf(state->logFile, "LAUNCH DETECTED: %f s\n", launchTime);
        free(meanAndVariance);
        return 1;
    }
    free(meanAndVariance);
    return 0;
}

int checkLanding(ProgramState *state)
{
    if (CUR_TIME_DOUBLE - front(state->timeQueue) < 0.5 * LANDING_DURATION)
    {
        return 0;
    }
    double curProportion = getProportionGtThreshold(state->accelQueue);
    printf("Cur Proportion: %f\n", curProportion);
    if (curProportion > LANDING_PROPORTION_THRESHOLD)
    {
        return 0;
    }

    double *meanAndVariance = getMeanAndVariance(state->accelQueue);
    printf("Mean: %f\tVariance: %f\n", meanAndVariance[0], meanAndVariance[1]);
    if (meanAndVariance[1] < LANDING_VARIANCE_THRESHOLD)
    {
        double landingTime = CUR_TIME_DOUBLE - state->programStart;
        printf("LANDING DETECTED: %f s\n", landingTime);
        fprintf(state->logFile, "LANDING DETECTED: %f s\n", landingTime);
        free(meanAndVariance);
        return 1;
    }
    free(meanAndVariance);

    return 0;
}

int writeIMUData(ProgramState *state)
{
    // TODO
    fprintf(state->imuDataFile, "%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f,%5.3f", CUR_TIME_DOUBLE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    return 0;
}

int autoSaveFiles(ProgramState *state)
{
    fclose(state->logFile);
    fclose(state->imuDataFile);
    printf("Saving files at %f s\n", CUR_TIME_DOUBLE - state->programStart);
    state->logFile = openFile("log", "txt");
    state->imuDataFile = openFile("imu_data", "csv");
    return 0;
}