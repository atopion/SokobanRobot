//
// Created by atopi on 02.12.2018.
//

#include <vector>
#include <queue>
#include <list>
#include "AssignmentAlgorithms.h"
#include "hungarian/Hungarian.h"
#include "Metrics.h"

AssignmentAlgorithms::AssignmentAlgorithms(int width, int height, int box_count, int *targets, int target_count, int *clearedBoard)
: metrics(width, height, targets, target_count, clearedBoard)
{
    AssignmentAlgorithms::width = width;
    AssignmentAlgorithms::height = height;
    AssignmentAlgorithms::box_count = box_count;
    AssignmentAlgorithms::targets = targets;
    AssignmentAlgorithms::target_count = target_count;
}

AssignmentAlgorithms::~AssignmentAlgorithms()
{

}

int AssignmentAlgorithms::closedAssignment(int *box_array)
{
    int result = 0;
    for(int i = 0; i < box_count; i++)
    {
        int min_dist = 1000000;
        for(int j = 0; j < target_count; j++)
        {
            int d = metrics.pull_distance(targets[j], box_array[i]);
            if(d < min_dist)
                min_dist = d;
        }
        result += min_dist;
    }
    return result;
}

int AssignmentAlgorithms::hungarianAssignment(int *box_array)
{
    std::vector<std::vector<double>> dist_matrix = std::vector<std::vector<double>>(target_count);

    for(int i = 0; i < target_count; i++)
    {
        dist_matrix[i] = std::vector<double>(box_count);
        for(int j = 0; j < box_count; j++)
            dist_matrix[i][j] = metrics.pull_distance(targets[i], box_array[j]);
    }

    HungarianAlgorithm HungAlgo;
    std::vector<int> assignment;

    return (int) HungAlgo.Solve(dist_matrix, assignment);
}

typedef struct _Elem
{
    int dist, target, box;
} Elem;

//bool cmp(Elem &left, Elem &right){ return left.dist < right.dist; };
struct compareElem {
    bool operator()(const Elem left, const Elem right) const
    {
        return left.dist > right.dist;
    }
};

int AssignmentAlgorithms::greedyAssignment(int *box_array) {
    int distance = 0;
    int *m_boxes = new int[box_count];
    int *m_targets = new int[target_count];
    int box_index = 0, target_index = 0;

    //auto cmp = [](Elem &left, Elem &right) { return left.dist < right.dist; };
    std::priority_queue<Elem, std::vector<Elem>, compareElem/*decltype(&cmp)*/> queue = std::priority_queue<Elem, std::vector<Elem>, compareElem/*decltype(&cmp)*/>();

    for (int i = 0; i < box_count; i++)
        for (int j = 0; j < target_count; j++)
            queue.push({.dist = metrics.pull_distance(targets[j], box_array[i]), .target = targets[i], .box = box_array[j]});

    while(!queue.empty())
    {
        Elem e = queue.top(); queue.pop();
        for(int a = 0; a < box_index; a++) // e.box not in m_boxes
            if(m_boxes[a] == e.box)
                goto already_contained;    // e.box in m_boxes => ignore, continue outer loop
        for(int a = 0; a < target_index; a++)  // e.target not in m_targets
            if(m_targets[a] == e.target)
                goto already_contained;        // e.target in m_targets => ignore, continue outer loop

        distance += e.dist;
        m_boxes[box_index++] = e.box;
        m_targets[target_index++] = e.target;

        already_contained:;
    }

    for(int b = 0; b < box_count; b++) // TODO optimization: maybe hashtable on m_boxes, m_targets
    {
        for(int j = 0; j < box_index; j++) {
            if (m_boxes[j] == box_array[b]) {
                goto ignore_element;
            }
        }

        {
            int min = 1000000;
            for (int j = 0; j < target_count; j++) {
                int d = metrics.pull_distance(targets[j], box_array[b]);
                if (d < min)
                    min = d;
            }
            distance += min;
        }

        ignore_element:;
    }

    delete[] m_boxes;
    delete[] m_targets;

    return distance;
}