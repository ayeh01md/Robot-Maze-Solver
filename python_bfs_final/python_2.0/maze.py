from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.nd_dict = dict()  # key: index, value: the correspond node

        self.data_rows = np.shape(self.raw_data)[0]
        self.data_columns = np.shape(self.raw_data)[1]

        for i in range(self.data_rows):
            node = Node(int(self.raw_data[i, 0]))
            for j in range(1,5):
                if self.raw_data[i, j] >= 0 and self.raw_data[i, j] <= self.data_rows:
                    node.setSuccessor(int(self.raw_data[i, j]), j, int(self.raw_data[i, j+4]))
            self.nodes.append(node)

        for i in range(self.data_rows):
            for j in range(1,5):
                if self.raw_data[i, j] >= 0 and self.raw_data[i, j] <= self.data_rows:
                    if i+1 not in self.nd_dict:
                        self.nd_dict[i+1] = list()
                    self.nd_dict[i+1].append(int(self.raw_data[i, j]))

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.raw_data[0][0]    #1->0

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        explored= []
        path = self.find_end_pt(nd, explored)
        explored.append(path[-2])

        end_point = []
        for node in self.nd_dict.keys():
            if len(self.nd_dict[node]) < 2:
                end_point.append(node)
        
        while len(explored) != len(end_point):
            newpath = self.find_end_pt(path[-1], explored)
            path.pop(-1)
            for nd in newpath:
                path.append(nd)
            explored.append(path[-2])
        path[0] = int(path[0])    
        path.pop(-1)
        return path
            
    def find_end_pt(self, start, explored):
        end_point = []
        for node in self.nd_dict.keys():
            if len(self.nd_dict[node]) < 2:
                end_point.append(node)

        queue = [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            neighbours = self.nd_dict[node]

            for neighbour in neighbours:
                if neighbour not in explored:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if node in end_point:
                        return new_path   

    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        explored = []
        queue = [[nd_from]]

        if nd_from == nd_to:
            return nd_from
       
        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = self.getNodeDict()[node]
             
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    if neighbour == nd_to:
                        return new_path
                explored.append(node)
        
    
    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        dir_to = self.nodes[nd_from - 1].getDirection(nd_to)
        if car_dir == Direction(1):
            if dir_to == Direction(1):
                return 's'
            if dir_to == Direction(2):
                return 'b'
            if dir_to == Direction(3):
                return 'l'
            if dir_to == Direction(4):
                return 'r'

        if car_dir == Direction(2):
            if dir_to == Direction(1):
                return 'b'
            if dir_to == Direction(2):
                return 's'
            if dir_to == Direction(3):
                return 'r'
            if dir_to == Direction(4):
                return 'l'

        if car_dir == Direction(3):
            if dir_to == Direction(1):
                return 'r'
            if dir_to == Direction(2):
                return 'l'
            if dir_to == Direction(3):
                return 's'
            if dir_to == Direction(4):
                return 'b'

        if car_dir == Direction(4):
            if dir_to == Direction(1):
                return 'l'
            if dir_to == Direction(2):
                return 'r'
            if dir_to == Direction(3):
                return 'b'
            if dir_to == Direction(4):
                return 's'
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)
