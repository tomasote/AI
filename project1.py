import pandas as pd
import numpy as np
import time



class Node:
    def __init__(self, cost, state, f):
        self.cost = cost
        self.state = state
        self.path = []
        self.f = f
    
    def __str__(self):
        return (f"State: {self.state}\nLength of path = {len(self.path)}\nPath: {self.path}\nCost: {self.cost}\nF: {self.f}")
    
    def update_path(self, new_val):
        self.path = self.path + [new_val]
    def set_path(self, lst):
        self.path = lst
    def set_f(self, f):
        self.f = f


INFINITY = 9999999999999

FAILURE = "There is no path"

frontier = []
reached = []
df = pd.read_csv('100_nodes.csv')
w = 0.5
start_node_idx = 0
end_node_idx = 19
path = []
generated_nodes = []

def f(df, w, current_node_idx, end_node_idx, node):
    return(w * cost(node) + (1-w)*h(df, current_node_idx, end_node_idx))

def cost(node):
    return node.cost

def h(df, current_node_idx, end_node_idx):
    return np.abs(df.iloc[current_node_idx]['x'] - df.iloc[end_node_idx]['x']) + np.abs(df.iloc[current_node_idx]['y'] - df.iloc[end_node_idx]['y'])

def get_possible_directions(df, node_idx):
    row = df.iloc[node_idx]
    possible_destinations = []
    for i in range(3, 103):
        if row[i]:
            possible_destinations.append(i-3)
    return possible_destinations

def generate_children(df, w, lst, end_node_idx, parent):
    result = []
    for i in lst:
        cost = df.iloc[parent.state][i+3]
        node = Node(cost+parent.cost, i, f(df, w, i, end_node_idx, parent))
        node.set_f(f(df, w, i, end_node_idx, node))
        node.set_path(parent.path + [i])
        result.append(node)
        generated_nodes.append(node)
    return result

def search_for_state(state, lst):
    for idx, i in enumerate(lst):
        if state == i.state:
            return idx
    return -1

def select_best_node(df, w):
    fbest = INFINITY
    for idx, node in enumerate(frontier):
        if f(df, w, node.state, end_node_idx, node) < fbest:
            fbest = f(df, w, node.state, end_node_idx, node)
            ibest = idx
    node = frontier[ibest]
    del frontier[ibest]
    return node
    
def astar(df, w, start_node_idx, end_node_idx):
    init_node = Node(0, 0, 0)
    node = Node(0, start_node_idx, f(df, w, start_node_idx, end_node_idx, init_node))
    node.set_f(f(df, w, start_node_idx, end_node_idx, node))
    node.set_path([start_node_idx])
    frontier.append(node)
    reached.append(node)
    while len(frontier) > 0:
        node = select_best_node(df, w)
        if node.state == end_node_idx:
            return node
        child_list = generate_children(df, w, get_possible_directions(df, node.state), end_node_idx, node)
        for child in child_list:
            idx = search_for_state(child.state, reached)
            if idx == -1:
                frontier.append(child)
                reached.append(child)
            elif child.f < reached[idx].f:
                    reached[idx] = child
                    frontier.append(child)
    return FAILURE
    
print(astar(df, w, start_node_idx, end_node_idx))
print(f"Generated nodes: {len(generated_nodes)}")