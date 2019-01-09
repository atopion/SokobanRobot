//
// Created by atopi on 04.12.2018.
//

#ifndef SOKOBANSOLVER_NODE_H
#define SOKOBANSOLVER_NODE_H


#include "Move.h"
#include <list>

class Node
{
public:
    int *box_array;
    int box_count;
    int player_pos;
    Node *farther;
    Move *move;
    int lower_bound;
    std::list<Node *> sons;

    Node();
    Node(const Node& other);
    ~Node();

    Node& operator=(const Node& other);
};


#endif //SOKOBANSOLVER_NODE_H
