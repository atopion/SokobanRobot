//
// Created by atopi on 26.11.2018.
//

#ifndef SOKOBANSOLVER_MAP_H
#define SOKOBANSOLVER_MAP_H

#include <iostream>

class Map {
private:
    int width;
    int height;
    int size;
    std::string mapstring;
    int* map;
    int* clearedMap;
    int  player;
    int* boxArray;
    int* targetArray;
    int  boxCount;
    int  targetCount;

public:
    explicit Map(std::string &str);
    ~Map();
    void mapProduction();
    void printMap();
    void calculateReachableArea(int reachable[], int box_array[], int pos);
    // Provide an empty array of the size of map to visited
    bool canReach(int *visited, int box_array[], int pos, int index);
    // Use the array from canReach
    int  normalizedPlayerPosition(int *visited, int box_array[], int pos);

    int getWidth();
    int getHeight();
    int getSize();
    int getBoxCount();
    int getTargetsCount();
    int getPlayer();

    int* getClearedMap();
    int* getMap();
    int* getBoxArray();
    int* getTargetsArray();

};


#endif //SOKOBANSOLVER_MAP_H
