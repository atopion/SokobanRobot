#!/usr/bin/env python3
from Directions import Directions
import sys 
from Robot import Robot


def main():
    args = sys.argv[1]
    run(args)
        
def run (args):
    r = Robot()
    i = 0
    while i < len(args):
        print(args[i])
        c = args[i]
        count = 30
        #while i < len(args) and args[i] == c:
        #    count += 30
        #    i += 1
            
        if c == 'l':
            if i+1 < len(args):
                if args[i+1] == 'r':
                    r.turn(Directions.left, count, 1)
                else:
                    r.turn(Directions.left, count, 0)
            else:
                r.turn(Directions.left, count, 0)
        if c == 'r':
            if i+1 < len(args):
                if args[i+1] == 'l':
                    r.turn(Directions.right, count, 1)
                else:
                    r.turn(Directions.right, count,0)
            else:
                r.turn(Directions.right, count,0)
        if c == 'u':
            if i+1 < len(args):
                if args[i+1] == 'd':
                    r.turn(Directions.up, count, 1)
                else:
                    r.turn(Directions.up, count, 0)
            else:
                r.turn(Directions.up, count, 0)
        if c == 'd':
            if i+1 < len(args):
                if args[i+1] == 'u':
                    r.turn(Directions.down, count, 1)
                else:
                    r.turn(Directions.down, count, 0)
            else:
                r.turn(Directions.down, count, 0)
        i += 1

if __name__ == "__main__":
    main()
