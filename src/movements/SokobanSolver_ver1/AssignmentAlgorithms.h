//
// Created by atopi on 02.12.2018.
//

#ifndef SOKOBANSOLVER_ASSIGNMENTALGORITHMS_H
#define SOKOBANSOLVER_ASSIGNMENTALGORITHMS_H


#include "Metrics.h"

class AssignmentAlgorithms
{
private:
    int width;
    int height;
    int box_count;
    int target_count;
    int *targets;
    Metrics metrics;

public:
    AssignmentAlgorithms(int width, int height, int box_count, int *targets, int target_count, int *clearedBoard);
    ~AssignmentAlgorithms();

    int closedAssignment(int *box_array);
    int hungarianAssignment(int *box_array);
    int greedyAssignment(int *box_array);
};


#endif //SOKOBANSOLVER_ASSIGNMENTALGORITHMS_H
