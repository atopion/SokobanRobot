//
// Created by atopi on 27.11.2018.
//

#include "TranspositionTable.h"

TranspositionTable::TranspositionTable(int boxCount, int size)
{
    TranspositionTable::boxCount = boxCount;
    TranspositionTable::size = size;
    TranspositionTable::map = std::unordered_map<int, bool>();
    TranspositionTable::zobristTable = new int *[size];

    std::random_device rd; // obtain a random number from hardware
    std::mt19937 eng(rd()); // seed the generator
    std::uniform_int_distribution<> distr(0, 999999999); // define the range

    for(int i = 0; i < size; i++)
    {
        TranspositionTable::zobristTable[i] = new int[boxCount +1];
        for(int j = 0; j < boxCount +1; j++)
        {
            TranspositionTable::zobristTable[i][j] = distr(eng);
        }
    }
}

TranspositionTable::~TranspositionTable()
{
    for(int i = 0; i < size; i++)
    {
        delete[] TranspositionTable::zobristTable[i];
    }
    delete[] TranspositionTable::zobristTable;
}

bool TranspositionTable::empty()
{
    return TranspositionTable::map.empty();
}

int TranspositionTable::computeHash(int *boxArray, int playerPos)
{
    int h = 1;
    for(int i = 0; i < boxCount; i++)
    {
        h ^= zobristTable[boxArray[i]][i];
    }
    h ^= zobristTable[playerPos][boxCount];
    return h;
}

void TranspositionTable::insert(int hash)
{
    map[hash] = true;
}

void TranspositionTable::remove(int hash)
{
    map.erase(hash);
}

bool TranspositionTable::lookup(int hash)
{
    return map.find(hash) != map.end();
}