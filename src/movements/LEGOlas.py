#!/usr/bin/env python3
from Directions import Directions
import sys 
from Robot import Robot


def main():
    args = sys.argv[1]
    r = Robot()
    i = 0
    while i < len(args):
        print(args[i])
        c = args[i]
        count = 10
        i += 1
        while i < len(args) and args[i] == c:
            count += 10 
            i += 1
        print('count %d:'% count)
        if c == 'l':
            r.turn(Directions.left, count)
        if c == 'r':
            r.turn(Directions.right, count)
        if c == 'u':
            r.turn(Directions.up, count)
        if c == 'd':
            r.turn(Directions.down, count)

if __name__ == "__main__":
    main()
