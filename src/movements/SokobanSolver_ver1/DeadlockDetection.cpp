//
// Created by atopi on 27.11.2018.
//

#include <iostream>
#include "DeadlockDetection.h"

DeadlockDetection::DeadlockDetection(int *game_map, int size, int width, int *target_array, int targetCount)
{
    DeadlockDetection::game_map = game_map;
    DeadlockDetection::target_array = target_array;
    DeadlockDetection::size = size;
    DeadlockDetection::width = width;
    DeadlockDetection::targetCount = targetCount;
    DeadlockDetection::deadlock_array = new int[size];

    detect_pull();
}

DeadlockDetection::~DeadlockDetection()
{
    delete[] deadlock_array;
}

bool DeadlockDetection::lookup(int a)
{
    if(a < 0 || a >= size) return true;
    return deadlock_array[a] == 1;
}


void DeadlockDetection::detect_pull()
{
    int *vi = new int[size];
    for(int i = 0; i < size; i++)
        vi[i] = 0;

    for(int i = 0; i < targetCount; i++)
        DeadlockDetection::reku_pull(DeadlockDetection::target_array[i], vi);

    for(int i = 0; i < size; i++)
    {
        if (vi[i] == 0)
            DeadlockDetection::deadlock_array[i] = 1;
        else
            DeadlockDetection::deadlock_array[i] = 0;
    }
    delete[] vi;
}

void DeadlockDetection::reku_pull(int a, int *visited)
{
    if(a < 0 || a > size)
        return;
    if(visited[a] == 1)
        return;
    visited[a] = 1;
    if(game_map[a] == 4)
        return;

    if(a+2 < size && game_map[a+1] != 4 && game_map[a+2] != 4)
        reku_pull(a+1, visited);
    if(a-2 >= 0 && game_map[a-1] != 4 && game_map[a-2] != 4)
        reku_pull(a-1, visited);
    if(a + 2*width < size && game_map[a+width] != 4 && game_map[a+2*width] != 4)
        reku_pull(a+width, visited);
    if(a - 2*width >= 0 && game_map[a-width] != 4 && game_map[a-2*width] != 4)
        reku_pull(a-width, visited);
}


// DEBUG
void DeadlockDetection::printMap()
{
    for(int i = 0; i < size; i++)
    {
        std::cout << deadlock_array[i];
        if(i % width == width -1)
            std::cout << std::endl;
    }
}