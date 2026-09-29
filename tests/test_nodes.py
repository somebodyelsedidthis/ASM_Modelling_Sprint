import pytest
import numpy as np
from nodes import Node, create_nodes, create_elements, connectivity, force_matrix

##############
# Test: Node #
##############

def test_node_init_defaults():
    node = Node(1.0,2.0)
    assert node.x == 1.0
    assert node.y == 2.0
    assert node.F_x == 0.0
    assert node.F_y == 0.0

def test_node_init_with_forces():
    node = Node(1.0,2.0,F_x=100.0,F_y=30.0)
    assert node.x == 1.0
    assert node.y == 2.0
    assert node.F_x == 100.0
    assert node.F_y == 30.0

def test_node_properties():
    node = Node(3.0,4.0,F_x=100.0,F_y=30.0)
    np.testing.assert_array_equal(node.coords, np.array([3.0,4.0]))
    np.testing.assert_array_equal(node.forces, np.array([100.0,30.0]))

######################
# Test: create_nodes #
######################

def test_create_nodes_valid():
    info = [
        {'x': 0.0, 'y': 0.0, 'C_x': False, 'C_y': False},
        {'x': 1.0, 'y': 0.0, 'C_x': True, 'C_y': False, 'F_x': 5.0, 'F_y': 5.0}
    ]

    nodes = create_nodes(info)

    assert len(nodes) == 2
    assert nodes[0].x == 0.0
    assert nodes[0].C_x is False
    assert nodes[1].x == 1.0
    assert nodes[1].C_x is True
    assert nodes[1].F_x == 5.0

def test_create_nodes_missing_keys():
    info = [
        {'x': 0.0},
        {'x': 1.0, 'y': 0.0, 'F_x': 5.0, 'F_y': 5.0}
    ]
    with pytest.raises(ValueError):
        create_nodes(info)

def test_create_nodes_unexpected_keys():
    info = [
        {'x': 0.0, 'y': 0.0, 'z': 3.0},
        {'x': 1.0, 'y': 0.0, 'F_x': 5.0, 'F_y': 5.0}
    ]
    with pytest.raises(ValueError):
        create_nodes(info)

#########################
# Test: create_elements #
#########################

def test_create_elements_valid():
    info = [
        {'node_i': 0, 'node_j': 1, 'E': 70e9, 'A': 0.01},
        {'node_i': 1, 'node_j': 2, 'E': 70e9, 'A': 0.01, 'element_type': 'frame'}
    ]
    elements = create_elements(info)
    assert len(elements) == 2
    assert elements[0].node_i == 0
    assert elements[1].element_type == 'frame'

def test_create_elements_missing_keys():
    info = [
        {'node_i': 0, 'node_j': 1, 'E': 70e9},
        {'node_i': 1, 'node_j': 2, 'E': 70e9, 'A': 0.01, 'element_type': 'frame'}
    ]
    with pytest.raises(ValueError):
        create_elements(info)

def test_create_elements_unexpected_keys():
    info = [
        {'node_i': 0, 'node_j': 1, 'E': 70e9, 'A': 0.01, 'B': 25},
        {'node_i': 1, 'node_j': 2, 'E': 70e9, 'A': 0.01, 'element_type': 'frame'}
    ]
    with pytest.raises(ValueError):
        create_elements(info)

######################
# Test: connectivity #
######################

def test_connectivity():
    element_info = [
        {'node_i': 0, 'node_j': 1, 'E': 70e9, 'A': 0.01},
        {'node_i': 1, 'node_j': 2, 'E': 70e9, 'A': 0.01},
        {'node_i': 2, 'node_j': 3, 'E': 70e9, 'A': 0.01}
    ]
    elements = create_elements(element_info)
    conn = connectivity(elements)

    expected = np.array([
        [0,1],
        [1,2],
        [2,3]
    ])

    assert conn.shape == (3,2)
    np.testing.assert_array_equal(conn, expected)

######################
# Test: force_matrix #
######################

def test_force_matrix():
    node_info = [
        {
            'x': 0.0,
            'y': 0.0,
            'C_x': False,
            'C_y': False,
            'F_x': 0.0,
            'F_y': 5.0
        },
        {
            'x': 5.0,
            'y': 3.0,
            'C_x': False,
            'C_y': False,
            'F_x': 10.0,
            'F_y': -25.0
        }
    ]

    nodes = create_nodes(node_info)
    F = force_matrix(nodes)

    expected = np.array([
        [0.0],
        [5.0],
        [10.0],
        [-25.0]
    ])

    assert F.shape == (4, 1)
    np.testing.assert_array_equal(F, expected)
