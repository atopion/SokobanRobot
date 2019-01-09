//
// Created by atopi on 27.11.2018.
//

#ifndef SOKOBANSOLVER_TRANSPOSITIONTABLE_H
#define SOKOBANSOLVER_TRANSPOSITIONTABLE_H


#include <unordered_map>
#include <random>


class TranspositionTable {
private:
    std::unordered_map<int, bool> map;
    int **zobristTable;
    int boxCount;
    int size;

public:
    TranspositionTable(int boxCount, int size);
    ~TranspositionTable();
    bool empty();
    int computeHash(int *boxArray, int playerPos);
    void insert(int hash);
    void remove(int hash);
    bool lookup(int hash);
};


#endif //SOKOBANSOLVER_TRANSPOSITIONTABLE_H
