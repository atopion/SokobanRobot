cmake_minimum_required(VERSION 3.12)
project(SokobanSolver)

set(CMAKE_CXX_STANDARD 11)
add_definitions("-g")

add_executable(SokobanSolver main.cpp Map.cpp Map.h TranspositionTable.cpp TranspositionTable.h DeadlockDetection.cpp DeadlockDetection.h Metrics.cpp Metrics.h AssignmentAlgorithms.cpp AssignmentAlgorithms.h Execution.cpp Execution.h Node.cpp Node.h hungarian/Hungarian.cpp hungarian/Hungarian.h)
