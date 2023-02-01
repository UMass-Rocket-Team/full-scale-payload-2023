#ifndef QUEUE_H
#define QUEUE_H
typedef struct
{
    int front, rear, size, capacity;
    double threshold;
    int numGtThreshold;
    double *array;
} Queue;

/**
 * @brief Create a Queue object
 * 
 * @param capacity The maximum capacity of the queue
 * @param threshold The threshold used to compute the proportion of values greater than the threshold
 * @return Queue* 
 */
Queue *createQueue(int capacity, double threshold);
int computeMaxCapacity(double updateInterval, double queueInterval);
int isFull(Queue *queue);
int isEmpty(Queue *queue);
/**
 * @brief Enqueues an item to the queue
 * 
 * @param queue 
 * @param item 
 * @return int 
 */
int enqueue(Queue *queue, double item);
/**
 * @brief Dequeues an item from the queue
 * 
 * @param queue 
 * @return double 
 */
double dequeue(Queue *queue);
double front(Queue *queue);
double rear(Queue *queue);
double getProportionGtThreshold(Queue *queue);
/**
 * @brief Reduces the queue to a single value
 * 
 * @param queue 
 * @param f 
 * @param init 
 * @param args 
 * @return double 
 */
double queueReduce(Queue *queue, double (*f)(double, double, double *), double init, double *args);
/**
 * @brief Get the mean and variance of the queue
 * 
 * @param queue 
 * @return double* 
 */
double *getMeanAndVariance(Queue *queue);
double printDouble(double acc, double d, double *args);
/**
 * @brief Resets the queue to its initial state
 * 
 * @param queue 
 */
void resetQueue(Queue *queue);

#endif