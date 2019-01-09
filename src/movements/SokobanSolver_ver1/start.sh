#!/bin/sh
arm-linux-gnueabi-g++ -o SokobanSolver -g -O3 --std=c++14 main.cpp Map.cpp Map.h TranspositionTable.cpp TranspositionTable.h DeadlockDetection.cpp DeadlockDetection.h Metrics.cpp Metrics.h AssignmentAlgorithms.cpp AssignmentAlgorithms.h Execution.cpp Execution.h Node.cpp Node.h hungarian/Hungarian.cpp hungarian/Hungarian.h
./SokobanSolver
