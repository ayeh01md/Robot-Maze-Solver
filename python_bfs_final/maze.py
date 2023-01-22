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
            print(node.getIndex())
            for j in range(1,5):
                if self.raw_data[i, j] >= 0 and self.raw_data[i, j] <= self.raw_data[self.data_rows - 1, 0]:
                    node.setSuccessor(int(self.raw_data[i, j]), j, int(self.raw_data[i, j+4]))
            self.nodes.append(node)

        for i in range(self.data_rows):
            for j in range(1,5):
                if self.raw_data[i, j] >= 0 and self.raw_data[i, j] <= self.raw_data[self.data_rows - 1, 0]:
                    index = self.raw_data[i, 0]
                    if index not in self.nd_dict:
                        self.nd_dict[index] = list()
                    self.nd_dict[index].append(int(self.raw_data[i, j]))

    def getNodeDict(self):
        return self.nd_dict

    def get_node(self, nd_idx):
        for node in self.nodes:
            if node.getIndex() == nd_idx:
                return node

    def get_point(self, nd):
        if nd % 6 == 0:
            return (nd / 6 - 1) * 30
        else:
            return (int(nd / 6) + 6 - nd % 6) * 30

    def find_the_most_efficient(self, start, end_point):
        the_min_dis = 100
        for i in range(len(end_point)):
            shortest_path = self.find_shortest_path(start, end_point[i])
            if (self.get_point(end_point[i]) / (len(shortest_path) - 1)) >= 30:
                if (len(shortest_path) - 1) < the_min_dis:
                    the_most_efficient = end_point[i]
                    the_min_dis = len(shortest_path) - 1
                    

        if the_min_dis == 100:
            for i in range(len(end_point)):
                shortest_path = self.find_shortest_path(start, end_point[i])
                if (len(shortest_path) - 1) < the_min_dis:
                    the_most_efficient = end_point[i]
                    the_min_dis = len(shortest_path) - 1

        return the_most_efficient

    def BFS(self, start_nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        end_point = []
        for node in self.nd_dict.keys():
            if len(self.nd_dict[node]) < 2:
                end_point.append(node)
        end_point.remove(start_nd)

        the_most_ef = self.find_the_most_efficient(start_nd, end_point)
        path = self.find_shortest_path(start_nd, the_most_ef)
        while len(end_point) > 1:
            end_point.remove(path[-1])
            the_most_ef = self.find_the_most_efficient(path[-1], end_point)
            newpath = self.find_shortest_path(path[-1], the_most_ef)
            path.pop(-1)
            for nd in newpath:
                path.append(nd)

        return path

    def find_shortest_path(self, nd_from, nd_to):
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
        dir_to = self.get_node(nd_from).getDirection(nd_to)
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
        return self.find_shortest_path(nd_from, nd_to)
