import pandas as pd
import numpy as np

class Node:
    #Might not use
    def __init__(self, cost, state, path, f):
        self.cost = cost
        self.state = state
        self.path = path
        self.f = f

def f(df, w, current_node_idx, end_node_idx):
    return(w * cost(df, current_node_idx, end_node_idx) + (1-w)*h(df, current_node_idx, end_node_idx))

def cost(df, current_node, other_node):
    return df.iloc[current_node][other_node + 3]

def h(df, current_node_idx, end_node_idx):
    return np.abs(df.iloc[current_node_idx]['x'] - df.iloc[end_node_idx]['x']) + np.abs(df.iloc[current_node_idx]['y'] - df.iloc[end_node_idx]['y'])

def get_possible_directions(df, node_idx):
    row = df.iloc[node_idx]
    possible_destinations = []
    for i in range(3, 103):
        if row[i]:
            possible_destinations.append(i-3)
    return possible_destinations
    


df = pd.read_csv('100_nodes.csv')
w = 0.5
start_node = 0
end_node = 1

print(df)
#print(h(df, 1, 2))
#print(get_possible_directions(df, 0))
#print(cost(df, 0, 1))
#print(f(df, 0.5, 99, 99))