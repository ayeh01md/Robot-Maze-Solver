from node import *
import maze as mz
import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("data\medium_maze.csv")
    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    interf = interface.interface()
    # TODO : Initialize necessary variables
    #print("Mode 0: for treasure-hunting")
    # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
    start_nd = maze.getStartPoint()
    path = maze.strategy(start_nd)
    path[0] = int(path[0])
    print(path)
    command = 's'
    command_list = []
    car_dirc = maze.nodes[path[0] - 1].getDirection(path[1])    
    for i in range(1,len(path) - 1):
        print(car_dirc)
        print(command)
        command_list.append(command)
        command = maze.getAction(car_dirc, path[i], path[i + 1])
        car_dirc = maze.nodes[path[i] - 1].getDirection(path[i + 1])
        if i != 0:
            print(i)
            interf.send_action(command)
    print(command_list)        
            
    #elif (sys.argv[1] == '1'):
        #print("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

if __name__ == '__main__':
    main()
