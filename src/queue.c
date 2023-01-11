// C program for array implementation of queue
#include <float.h>
#include <stdio.h>
#include <stdlib.h>
#include "../include/queue.h"
// A structure to represent a queue

Queue *createQueue(int capacity, double threshold)
{
    Queue *queue = malloc(sizeof *queue);
    queue->capacity = capacity;
    queue->front = queue->size = 0;
    queue->rear = capacity - 1;
    queue->threshold = threshold;
    queue->numGtThreshold = 0;
    queue->array = malloc(sizeof *queue->array * queue->capacity);
    return queue;
}

int computeMaxCapacity(double updateInterval, double queueInterval)
{
    return (int)(queueInterval / updateInterval * 1.25);
}
// Queue is full when size becomes
// equal to the capacity
int isFull(Queue *queue)
{
    return (queue->size == queue->capacity);
}

// Queue is empty when size is 0
int isEmpty(Queue *queue)
{
    return (queue->size == 0);
}

// Function to add an item to the queue.
// It changes rear and size
int enqueue(Queue *queue, double item)
{
    if (queue->size == queue->capacity)
    {
        return 1;
    }
    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->array[queue->rear] = item;
    queue->size = queue->size + 1;
    if (item > queue->threshold)
    {
        queue->numGtThreshold++;
    }
    return 0;
}

// Function to remove an item from queue.
// It changes front and size
double dequeue(Queue *queue)
{
    if (queue->size == 0)
    {
        return DBL_MAX;
    }
    double item = queue->array[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size = queue->size - 1;
    if (item > queue->threshold)
    {
        queue->numGtThreshold--;
    }
    return item;
}

// Function to get front of queue
double front(Queue *queue)
{
    if (queue->size == 0)
    {
        return DBL_MAX;
    }
    return queue->array[queue->front];
}

// Function to get rear of queue
double rear(Queue *queue)
{
    if (queue->size == 0)
    {
        return DBL_MAX;
    }
    return queue->array[queue->rear];
}

double queueReduce(Queue *queue, double (*f)(double, double, double *), double init, double *args)
{
    double acc = init;
    for (int i = 0; i < queue->size; i++)
    {
        acc = f(acc, queue->array[(queue->front + i) % queue->capacity], args);
    }
    return acc;
}
double printDouble(double acc, double d, double *args)
{
    (void)args;
    printf("%3.3f ", d);
    return acc;
}

double getProportionGtThreshold(Queue *queue)
{
    if (queue->size == 0)
    {
        return 0;
    }
    return (double)queue->numGtThreshold / (double)queue->size;
}

double meanHelper(double acc, double d, double *args)
{
    (void)args;
    return acc + d;
}

double varianceHelper(double acc, double d, double *args)
{
    (void)args;
    return acc + (d - args[0]) * (d - args[0]);
}

double *getMeanAndVariance(Queue *queue)
{
    if (queue->size == 0)
    {
        return 0;
    }
    double *output = malloc(sizeof *output * 2);
    output[0] = queueReduce(queue, meanHelper, 0, 0) / queue->size;
    output[1] = queueReduce(queue, varianceHelper, 0, output) / queue->size;
    return output;
}

void resetQueue(Queue *queue)
{
    free(queue->array);
    queue->array = NULL;
    free(queue);
    queue = NULL;
}
