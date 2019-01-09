#include <iostream>
#include <fstream>
#include <sstream>
#include <chrono>
#include <unistd.h>
#include "Map.h"
#include "TranspositionTable.h"
#include "Node.h"
#include "Execution.h"

int main() {
    std::string level_name = "level3.txt", path = "/src/level/", line, level;
    std::stringstream stream;

    std::ifstream file;
    file.open(path + level_name);

    while(std::getline(file, line))
        stream << line << std::endl;
    file.close();
    level = stream.str();

    std::chrono::high_resolution_clock::time_point start = std::chrono::high_resolution_clock::now();
    Map game_map = Map(level);
    game_map.mapProduction();
    game_map.printMap();

    Node root = Node();
    root.box_array = game_map.getBoxArray();
    root.player_pos = game_map.getPlayer();
    root.lower_bound = 10000;
    root.sons = std::list<Node *>();

    Execution exec = Execution(game_map);
    Node *tmp;
    std::chrono::high_resolution_clock::time_point end   = std::chrono::high_resolution_clock::now();
    std::cout << "Preparation time: " << std::chrono::duration_cast<std::chrono::milliseconds>( end - start ).count() << " ms" << std::endl;

    start = std::chrono::high_resolution_clock::now();
    Node *solution = exec.execute(&root);
    end   = std::chrono::high_resolution_clock::now();
    std::cout << "Execution time:   " << std::chrono::duration_cast<std::chrono::milliseconds>( end - start ).count() << " ms" << std::endl;

    if(solution == nullptr)
        std::cout << "No solution found" << std::endl;
    else
    {
        std::string result;
        while(solution->farther != nullptr)
        {
            result.insert(0, Move::str(*(solution->move)) + ", ");
            tmp = solution->farther;
            delete solution;
            solution = tmp;
        }
        result.erase(result.size()-2, 1).erase(result.size()-1, 1).erase(result.size()-2, 1);
        result = "[" + result + "]";

        std::cout << "Solution found: " << result << std::endl;
    }
}
