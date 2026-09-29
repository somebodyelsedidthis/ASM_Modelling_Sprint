import pytest
import main

node_info = [
    {'x':0.1,'y':0.0, 'C_x': True, 'C_y': True},
    {'x':0.0,'y':0.1, 'C_x': True},
    {'x':0.1,'y':0.15, 'F_x': 1500, 'F_y': -2500},
    {'x':0.2,'y':0.05, 'C_x': True}
]
element_info = [
    {'node_i':0,'node_j':1,'E':70e9,'A':1e-5},
    {'node_i':1,'node_j':2,'E':70e9,'A':1e-5},
    {'node_i':2,'node_j':3,'E':70e9,'A':1e-5},
    {'node_i':0,'node_j':3,'E':70e9,'A':1e-5},
    {'node_i':0,'node_j':2,'E':70e9,'A':2e-5}
]

print(main.main(node_info, element_info))