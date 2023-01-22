import pandas as pd
import numpy as np

raw_data = pd.read_csv('data\small_maze.csv').values

nd_dict = dict()  # key: index, value: the correspond node

data_rows = np.shape(raw_data)[0]
data_columns = np.shape(raw_data)[1]

for i in range(data_rows):
    for j in range(1,5):
        if raw_data[i, j] >= 0 and raw_data[i, j] <= data_rows:
            if i+1 not in nd_dict:
                nd_dict[i+1] = list()
            nd_dict[i+1].append(raw_data[i, j])


if (len(nd_dict) < 2):
    print("Error: the start point is not included.")

else:
    print(raw_data[0][0])
print(nd_dict)

nd = 40
print(int(nd / 6))