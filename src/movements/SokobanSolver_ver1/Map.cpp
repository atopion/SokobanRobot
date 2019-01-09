//
// Created by atopi on 26.11.2018.
//

#include <sstream>
#include <iomanip>
#include <vector>
#include "Map.h"

Map::Map(std::string &str)
{
    width = 0;
    height = 0;
    size = str.size();
    for(char c : str) if(c == '\n') size--;
    Map::mapstring = str;
    Map::map = new int[size]; //(int *) malloc(str.size());
    Map::clearedMap = new int[size];
    Map::player = 0;
}

Map::~Map()
{
    delete[] Map::map; //free(Map::map);
}

void Map::mapProduction()
{
    int tmp = 0, j = 0;
    std::vector<int> boxes, targets;
    for(char c : mapstring)
    {
        tmp++;
        switch (c)
        {
            case '@': // Player
                map[j] = 1;
                clearedMap[j] = 5;
                player = j;
                j++;
                break;
            case '$': // Box
                map[j] = 2;
                clearedMap[j] = 5;
                boxes.push_back(j);
                j++;
                break;
            case '.': // Target
                map[j] = 3;
                clearedMap[j] = 3;
                targets.push_back(j);
                j++;
                break;
            case '#': // Wall
                map[j] = 4;
                clearedMap[j] = 4;
                j++;
                break;
            case ' ': // Empty
                map[j] = 5;
                clearedMap[j] = 5;
                j++;
                break;

            case '\n': // New line
                if(tmp-2 > width)
                {
                    width = tmp-2;
                }
                tmp = 0;
                break;

            default:
                break;
        }
    }
    size = j;
    height = size / width;

    boxArray = new int[boxes.size()];
    boxCount = boxes.size();
    for(int i = 0; i < boxes.size(); i++) boxArray[i] = boxes[i];
    targetArray = new int[targets.size()];
    targetCount = targets.size();
    for(int i = 0; i < targets.size(); i++) targetArray[i] = targets[i];
}

void Map::printMap()
{
    std::stringstream ss;
    for(int i = 0; i < size; i++)
    {
        switch (map[i])
        {
            case 1:
                std::cout << "@";
                break;
            case 2:
                std::cout << "$";
                break;
            case 3:
                std::cout << ".";
                break;
            case 4:
                std::cout << "#";
                break;
            case 5:
                std::cout << " ";
                break;

            default:
                break;
        }
        ss << ' ' << std::setfill('0') << std::setw(2) << i;

        if(i % width == width-1)
        {
            std::cout << "   " << ss.str() << std::endl;
            ss.str(std::string());
        }
    }
}

void Map::calculateReachableArea(int reachable[], int box_array[], int pos)
{
    if((pos < 0) || (pos > size) || reachable[pos] == 1 || map[pos] == 4)
        return;
    for(int i = 0; i < boxCount; i++)
        if(box_array[i] == pos)
            return;

    reachable[pos] = 1;
    Map::calculateReachableArea(reachable, box_array, pos + 1);
    Map::calculateReachableArea(reachable, box_array, pos - 1);
    Map::calculateReachableArea(reachable, box_array, pos + width);
    Map::calculateReachableArea(reachable, box_array, pos - width);
}

bool Map::canReach(int *visited, int box_array[], int pos, int index)
{
    for(int i = 0; i < size; i++)
        visited[i] = 0;
    Map::calculateReachableArea(visited, box_array, pos);
    return visited[index] == 1;
}

int Map::normalizedPlayerPosition(int *visited, int *box_array, int pos)
{
    for(int i = 0; i < size; i++)
        if(visited[i] == 1)
            return i;
    return 0;
}

int Map::getWidth() { return width; }
int Map::getHeight() { return height; }
int Map::getSize() { return size; }
int Map::getBoxCount() { return boxCount; }
int Map::getTargetsCount() { return targetCount; }
int Map::getPlayer() { return player; }

int* Map::getClearedMap() { return clearedMap; }
int* Map::getMap() { return map; }
int* Map::getBoxArray() { return boxArray; }
int* Map::getTargetsArray() { return targetArray; }
