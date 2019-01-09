//
// Created by atopi on 03.12.2018.
//

#include "Execution.h"
#include <stdio.h>
#include <list>

Execution::Execution(Map &map) : transpositionTable(map.getBoxCount(), map.getSize()),
assignmentAlgorithms(map.getWidth(), map.getHeight(), map.getBoxCount(), map.getTargetsArray(), map.getTargetsCount(), map.getClearedMap()),
deadlockDetection(map.getClearedMap(), map.getSize(), map.getWidth(), map.getTargetsArray(), map.getTargetsCount())
{
    Execution::map = &map;
    Execution::width = map.getWidth();
    Execution::height = map.getHeight();
    Execution::clearedMap = map.getClearedMap();
    Execution::size = map.getSize();
    Execution::boxCount = map.getBoxCount();

    Execution::transpositionTable.insert(transpositionTable.computeHash(map.getBoxArray(), map.getPlayer()));

}

bool Execution::cont(int *array, int size, int item)
{
    for(int i = 0; i < size; i++)
        if(array[i] == item)
            return true;
    return false;
}

Move **Execution::possibleMoves(int box, int *boxes)
{
    Move **result = new Move*[4];
    for(int i = 0; i < 4; i++)
        result[i] = new Move;

    int i = 0;
    for(int a : {-1, 1, -width, width})
    {
        if(0 <= (box + a) <= size && clearedMap[box + a] != 4 && clearedMap[box - a] != 4 && !cont(boxes, map->getBoxCount(), box + a)
            && !cont(boxes, map->getBoxCount(), box - a) && !deadlockDetection.lookup(box + a))
            *result[i++] = {.from = box, .to = box + a};
        else
            *result[i++] = {0, 0};
    }
    return result;
}

Node *Execution::analyseState(Node *node)
{
    int *box_array = node->box_array;
    int *vi = new int[size];

    for(int i = 0; i < boxCount; i++)
    {
        Move **m = possibleMoves(box_array[i], box_array);
        for(int j = 0; j < 4; j++)
        {
            if(m[j]->to == 0 && m[j]->from == 0)
                continue;

            if(deadlockDetection.lookup(m[j]->to))
                continue;

            if(!map->canReach(vi, box_array, node->player_pos, m[j]->from - (m[j]->to - m[j]->from)))
                continue;

            int *new_box_array = new int[boxCount];
            for(int k = 0; k < boxCount; k++)
                new_box_array[k] = box_array[k];
            new_box_array[i] = m[j]->to;
            int pos = map->normalizedPlayerPosition(vi, new_box_array, m[j]->from);

            if(transpositionTable.lookup(transpositionTable.computeHash(new_box_array, pos)))
                continue;
            transpositionTable.insert(transpositionTable.computeHash(new_box_array, pos));

            int bound = assignmentAlgorithms.hungarianAssignment(new_box_array);

            Node* n = new Node;
            n->box_array = new_box_array;
            n->player_pos = m[j]->from;
            n->farther = node;
            n->move = m[j];
            n->lower_bound = bound;
            n->sons = std::list<Node*>();

            if(bound == 0)
            {
                delete[] vi;
                return n;
            }

            std::list<Node *>::iterator it;
            for(it = node->sons.begin(); it != node->sons.end(); it++)
            {
                if(bound < (*it)->lower_bound)
                {
                    node->sons.insert(it, n);
                    goto inserted;  // Dont append if already added
                }
            }
            node->sons.push_back(n);
            inserted:;
        }
    }
    delete[] vi;
    return nullptr;
}

Node *Execution::execute(Node *current_node, int depth)
{
    Node *res = analyseState(current_node);

    if(res != nullptr)
    {
        std::cout << "Final depth: " << depth << std::endl;
        return res;
    }
    if(current_node->sons.empty())
    {
        //std::cout << "No sons (depth=" << depth << ")" << std::endl;
        return nullptr;
    }
    if(depth >= 1000)
    {
        std::cout << "Maximum depth reached. Aborting." << std::endl;
        return nullptr;
    }

    std::list<Node *>::iterator it;
    for(it = current_node->sons.begin(); it != current_node->sons.end(); it++)
    {
        Node *r = execute(*it, depth +1);
        if(r != nullptr)
            return r;
        else
            delete r;
    }
    return nullptr;
}

// DEBUG
void Execution::printDeadlockMap()
{
    deadlockDetection.printMap();
}