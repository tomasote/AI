import pandas as pd
import numpy as np

class Node:
    def __init__(self, cost, state, f):
        self.cost = cost
        self.state = state
        self.path = []
        self.f = f
    
    def __str__(self):
        return (f"Length of path = {len(self.path)}\nPath: {self.path}")
    
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
start_node_idx = 99
end_node_idx = 0
generated_nodes = []

def f(df, w, current_node_idx, end_node_idx, current_node):
    return(w * cost(current_node) + (1-w)*h(df, current_node_idx, end_node_idx))

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

def generate_children(df, w, end_node_idx, parent):
    result = []
    lst = get_possible_directions(df, parent.state)
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

def select_best_node():
    fbest = INFINITY
    for idx, node in enumerate(frontier):
        if node.f < fbest:
            fbest = node.f
            ibest = idx
    node = frontier[ibest]
    del frontier[ibest]
    return node
    
def astar(df, w, start_node_idx, end_node_idx):
    init_node = Node(0, 0, 0) #Dummy node
    node = Node(0, start_node_idx, f(df, w, start_node_idx, end_node_idx, init_node))
    generated_nodes.append(node)
    node.set_f(f(df, w, start_node_idx, end_node_idx, node))
    node.set_path([start_node_idx])
    frontier.append(node)
    reached.append(node)
    while len(frontier) > 0:
        node = select_best_node()
        if node.state == end_node_idx:
            return node
        child_list = generate_children(df, w, end_node_idx, node)
        for child in child_list:
            idx = search_for_state(child.state, reached)
            if idx == -1:
                frontier.append(child)
                reached.append(child)
            elif child.cost < reached[idx].cost:
                    reached[idx] = child
                    frontier.append(child)
    return FAILURE

wbool = False
startbool = False
stopbool = False

while(not wbool):
    try:
        w = float(input('Enter a weight parameter between 0 and 1: '))
        assert w >= 0 and w <= 1
    except KeyboardInterrupt:
        quit()
    except:
        print("Faulty weight parameter")
    else:
        wbool = True
while(not startbool):
    try:
        start_node_idx = int(input('Enter a starting node (index): '))
        assert start_node_idx >= 0 and start_node_idx <= 99 and isinstance(start_node_idx, int)
    except KeyboardInterrupt:
        quit()
    except:
        print("Faulty starting index parameter")
    else:
        startbool = True
while(not stopbool):
    try:
        end_node_idx = int(input('Enter a end node (index): '))
        assert end_node_idx >= 0 and end_node_idx <= 99 and isinstance(end_node_idx, int) and start_node_idx != end_node_idx
    except KeyboardInterrupt:
        quit()
    except:
        print("Faulty starting index parameter")
    else:
        stopbool = True

print("###############################################################################\n")
print(astar(df, w, start_node_idx, end_node_idx))
print(f"Generated nodes: {len(generated_nodes)}\n")
print("###############################################################################")