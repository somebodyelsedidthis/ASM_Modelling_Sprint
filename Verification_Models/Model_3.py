import sys
import os

# add parent directory to import path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import pytest
import main, elements, nodes, rotation, global_stiffness, solver, post_proc

node_info = [
    # Node 1
    {
        'x': 1.25,
        'y': 0.75,
        'D_x': 0,
        'D_y': 0
    },

    # Node 2
    {
        'x': 2.0,
        'y': 0.0,
        'D_x': None,
        'D_y': 0,
        'F_x': 1500.0
    },

    # Node 3
    {
        'x': 0.75,
        'y': 0.0,
        'D_x': 0,
        'D_y': 0
    },

    # Node 4
    {
        'x': 0.0,
        'y': 0.0,
        'D_x': None,
        'D_y': 0,
        'F_x': -500.0
    },

    # Node 5
    {
        'x': 0.5,
        'y': 0.5,
        'D_x': None,
        'D_y': None
    }
]


element_info = [
        # Element 1: Node 1 -> Node 2
    {
        'node_i': 0,
        'node_j': 1,
        'E': 70e9,
        'A': 5e-5
    },

    # Element 2: Node 3 -> Node 5
    {
        'node_i': 2,
        'node_j': 4,
        'E': 70e9,
        'A': 3e-5
    },

    # Element 3: Node 4 -> Node 5
    {
        'node_i': 3,
        'node_j': 4,
        'E': 70e9,
        'A': 3e-5
    },

    # Element 4: Node 1 -> Node 5
    {
        'node_i': 0,
        'node_j': 4,
        'E': 70e9,
        'A': 5e-5
    }
]

print(main.main(node_info, element_info))