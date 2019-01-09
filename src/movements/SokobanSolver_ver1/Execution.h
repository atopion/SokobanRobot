//
// Created by atopi on 03.12.2018.
//

#ifndef SOKOBANSOLVER_EXECUTION_H
#define SOKOBANSOLVER_EXECUTION_H


#include "Node.h"
#include "TranspositionTable.h"
#include "Map.h"
#include "AssignmentAlgorithms.h"
#include "DeadlockDetection.h"

class Execution
{
private:
    Map *map;
    int width;
    int height;
    int *clearedMap;
    int size;
    int boxCount;
    TranspositionTable transpositionTable;
    AssignmentAlgorithms assignmentAlgorithms;
    DeadlockDetection deadlockDetection;

public:
    Execution(Map &map);

    Move **possibleMoves(int box, int *box_array);
    Node *analyseState(Node *node);
    Node *execute(Node *current_node, int depth=0);

    bool cont(int *array, int size, int item);

    //DEBUG
    void printDeadlockMap();
};

#endif //SOKOBANSOLVER_EXECUTION_H
