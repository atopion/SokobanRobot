//
// Created by atopi on 04.12.2018.
//

#ifndef SOKOBANSOLVER_MOVE_H
#define SOKOBANSOLVER_MOVE_H

#include <string>

typedef struct _Move
{
    int from, to;

    static std::string str(_Move m)
    {
        return std::string("[" + std::to_string(m.from) + ", " + std::to_string(m.to) + "]");
    }
} Move;

#endif //SOKOBANSOLVER_MOVE_H
