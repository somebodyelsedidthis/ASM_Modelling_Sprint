import pytest
import main, elements, nodes, rotation, global_stiffness, solver, post_proc

node_info = [
    {'x':0.1,'y':0.0},
    {'x':0.0,'y':0.1, 'u_x': 0.0, 'u_y':1e-5},
    {'x':0.1,'y':0.15, 'F_x': 1500, 'F_y': -2500},
    {'x':0.2,'y':0.05}
]
element_info = [
    {'node_i':1,'node_j':2,'E':70e9,'A':1e-5},
    {'node_i':2,'node_j':3,'E':70e9,'A':1e-5},
    {'node_i':3,'node_j':4,'E':70e9,'A':1e-5},
    {'node_i':1,'node_j':4,'E':70e9,'A':1e-5},
    {'node_i':1,'node_j':3,'E':70e9,'A':2e-5}
]


print(main.main(node_info, element_info))