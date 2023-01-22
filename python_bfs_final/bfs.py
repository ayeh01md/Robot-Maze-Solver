import pandas as pd
import numpy as np
from node import *

data = pd.read_csv('data\maze_8x6_1.csv').values
nodes = []
nd_dict = dict()  # key: index, value: the correspond node

data_rows = np.shape(data)[0]
data_columns = np.shape(data)[1]

def get_point(nd):
    if nd % 6 == 0:
        return (nd / 6 - 1) * 30
    else:
        return (int(nd / 6) + 6 - nd % 6) * 30   

for i in range(data_rows):
    node = Node(data[i, 0])
    for j in range(1,5):
        if data[i, j] >= 0 and data[i, j] <= data_rows:
            node.setSuccessor(int(data[i, j]), j, int(data[i, j+4]))
    nodes.append(node)

for i in range(data_rows):
    for j in range(1,5):
        if data[i, j] >= 0 and data[i, j] <= data[data_rows - 1, 0]:
            index = data[i, 0]
            if index not in nd_dict:
                nd_dict[index] = list()
            nd_dict[index].append(int(data[i, j]))

end_point = []

for node in nd_dict.keys():
    if len(nd_dict[node]) < 2:
        end_point.append(node)

end_point.remove(6)

def find_the_most_efficient(nd_dict, start):
    the_min_dis = 100
    for i in range(len(end_point)):
        shortest_path = find_shortest_path(nd_dict, start, end_point[i])
        print(start, end_point[i], shortest_path, get_point(end_point[i]) / (len(shortest_path) - 1))
        if (get_point(end_point[i]) / (len(shortest_path) - 1)) >= 30:
            if (len(shortest_path) - 1) < the_min_dis:
                the_most_efficient = end_point[i]
                the_min_dis = len(shortest_path) - 1
                

    if the_min_dis == 100:
        for i in range(len(end_point)):
            shortest_path = find_shortest_path(nd_dict, start, end_point[i])
            if (len(shortest_path) - 1) < the_min_dis:
                the_most_efficient = end_point[i]
                the_min_dis = len(shortest_path) - 1

    return the_most_efficient

def BFS_1(nd_dict, start):
    the_most_ef = find_the_most_efficient(nd_dict, start)
    path = find_shortest_path(nd_dict, start, the_most_ef)
    print(path)
    while len(end_point) > 1:
        end_point.remove(path[-1])
        the_most_ef = find_the_most_efficient(nd_dict, path[-1])
        newpath = find_shortest_path(nd_dict, path[-1], the_most_ef)
        for nd in newpath:
            path.append(nd)
        
        
    path.pop(-1)
    return path

def find_end_pt(nd_dict, start):
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        neighbours = nd_dict[node]

        for neighbour in neighbours:
            
            new_path = list(path)
            new_path.append(neighbour)
            queue.append(new_path)

            if node in end_point:
                end_point.remove(node)
                return new_path

def find_shortest_path(nd_dict, nd_from, nd_to):
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
                neighbours = nd_dict[node]
             
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    if neighbour == nd_to:
                        return new_path
                explored.append(node)               
                
          
        


print(BFS_1(nd_dict, 6))

#print(nodes)
#print(nodes[0].getDirection(2))

#print(Direction(1))
#['A', 'B', 'D', 'E', 'C', 'F']


