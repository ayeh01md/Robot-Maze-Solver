from node import *
import maze as mz
from Server import Scoreboard
#import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os
import threading

def main():
    maze = mz.Maze("data\maze_8x6_1.csv")
    #point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    interf = interface.interface()
    path = maze.strategy(6)
    path[0] = int(path[0])
    print(path)
    command = 's'
    command_list = []
    car_dirc = maze.get_node(path[0]).getDirection(path[1])
    for i in range(1,len(path) - 1):
        print(car_dirc)
        print(command)
        command_list.append(command)
        command = maze.getAction(car_dirc, path[i], path[i + 1])
        car_dirc = maze.get_node(path[i]).getDirection(path[i + 1])
        if i != 0:
            interf.send_action(command)
    
    myScoreboard = Scoreboard('filepath','Group5',"http://140.112.175.15:3000")
    while True:
        if interf.get_UID() != 0:
            myScoreboard.add_UID(interf.get_UID())
            print(myScoreboard.getCurrentScore())
            
    
if __name__ == '__main__':
    main()
