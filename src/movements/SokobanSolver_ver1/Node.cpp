//
// Created by atopi on 04.12.2018.
//

#include "Node.h"
#include <list>
#include <iostream>
#include <cstring>

Node::~Node()
{
    std::list<Node *>::iterator it;
    for(it = sons.begin(); it != sons.end(); )
    {
        it = sons.erase(it);
    }
    delete move;
    delete box_array;
}

Node::Node(const Node& other)
{
    box_count = other.box_count;
    box_array = new int[box_count];
    std::memcpy(box_array, other.box_array, box_count);
    player_pos = other.player_pos;
    lower_bound = other.lower_bound;
    sons = other.sons;
    farther = other.farther;
    move = new Move();
    move->from = other.move->from;
    move->to = other.move->to;

}

Node::Node()
{
    box_count = 0;
    box_array = nullptr;
    player_pos = 0;
    lower_bound = 0;
    sons = std::list<Node *>();
    farther = nullptr;
    move = nullptr;
}

Node& Node::operator=(const Node& other)
{
    if(this != &other)
    {
        box_count = other.box_count;
        player_pos = other.player_pos;
        lower_bound = other.lower_bound;
        sons = other.sons;

        move = new Move();
        move->from = other.move->from;
        move->to = other.move->to;

        farther = other.farther;

        box_array = new int[box_count];
        std::memcpy(box_array, other.box_array, box_count);
    }
}