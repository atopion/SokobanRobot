//
// Created by atopi on 27.11.2018.
//

#ifndef SOKOBANSOLVER_DEADLOCKDETECTION_H
#define SOKOBANSOLVER_DEADLOCKDETECTION_H


class DeadlockDetection
{
private:
    int *game_map;
    int *target_array;
    int  size;
    int  width;
    int  targetCount;
    int *deadlock_array;

    void detect_pull();
    void reku_pull(int a, int *visited);

public:
    DeadlockDetection(int *game_map, int size, int width, int *target_array, int targetCount);
    ~DeadlockDetection();
    bool lookup(int a);

    // DEBUG
    void printMap();
};


#endif //SOKOBANSOLVER_DEADLOCKDETECTION_H
