//
// Created by atopi on 02.12.2018.
//

#include "Metrics.h"
#include <queue>
#include <cmath>
#include <iostream>

Metrics::Metrics(int width, int height, int *targets, int targets_count, int *clearedBoard)
{
    Metrics::width = width;
    Metrics::height = height;
    Metrics::targets_count = targets_count;
    Metrics::target_codes = new int[targets_count];

    Metrics::distance_to_goals = new int*[targets_count];
    for(int i = 0; i < targets_count; i++)
    {
        Metrics::distance_to_goals[i] = new int[width*height];
        for(int j = 0; j < width*height; j++)
            Metrics::distance_to_goals[i][j] = 32000;
    }

    std::queue<int> target_queue = std::queue<int>();

    for(int i = 0; i < targets_count; i++)
    {
        distance_to_goals[i][targets[i]] = 0;
        target_codes[i] = targets[i];
        target_queue.push(targets[i]);
        while(!target_queue.empty())
        {
            int pos = target_queue.front();
            target_queue.pop();
            for(int d : {-1, 1, -width, width})
            {
                int box_pos = pos + d;
                int player_pos = pos + 2*d;
                if(distance_to_goals[i][box_pos] == 32000 && clearedBoard[box_pos] != 4 && clearedBoard[player_pos] != 4)
                {
                    distance_to_goals[i][box_pos] = distance_to_goals[i][pos] + 1;
                    target_queue.push(box_pos);
                }
            }
        }
    }
}

Metrics::~Metrics()
{
    for(int i = 0; i < targets_count; i++)
        delete distance_to_goals[i];
    delete distance_to_goals;
}

int Metrics::manhattan_distance(int a, int b)
{
    return (int)(std::abs((a % width) - (a / width)) + std::abs((b % width) - (b % width)));
}

int Metrics::pythagoran_distance(int a, int b)
{
    return (int)(std::sqrt(((a % width) - (b % width))*((a % width) - (b % width)) + ((a / width) - (b / width))*((a / width) - (b / width))));
}

int Metrics::lookupTarget(int target)
{
    for(int i = 0; i < targets_count; i++)
        if(target_codes[i] == target)
            return i;

    return 0;
}

int Metrics::pull_distance(int target, int pos)
{
    return Metrics::distance_to_goals[lookupTarget(target)][pos];
}