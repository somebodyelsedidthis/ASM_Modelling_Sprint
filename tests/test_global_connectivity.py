import numpy as np
import pytest
import numpy.testing as nte
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from global_stiffness import TrussStructure
from elements import Element
from nodes import create_nodes, create_elements
from rotation import rotation_angles

@pytest.fixture
def elements():
    element_info = [{'node_i':2,
                            'node_j':3,
                            'E':70e9,
                            'A':10e-6},
                        {'node_i':1,
                            'node_j':2,
                            'E':70e9,
                            'A':10e-6}               
                            ]
    return create_elements(element_info=element_info)

@pytest.fixture
def nodes():
     node_info=[{'x':0.0,
                 'y':0.0},
                 {'x':125.0/1000,
                 'y':100.0/1000},
                 {'x':0.0,
                 'y':100.0/1000}]
     return create_nodes(node_info=node_info)
     
@pytest.fixture
def connectivity_matrix():
    return np.array([
         [3,2],
         [1,2],
    ])

@pytest.fixture
def angles():
    return rotation_angles(elements,
                           nodes)

@pytest.fixture
def truss_structure():
    return TrussStructure(np.array(elements),
                          np.array(nodes),
                          np.array(connectivity_matrix),
                          np.array(angles))

class TestGlobalStiffness:
    def test_transformation_matrix(self,
                                   truss_structure):
        truss_structure.assemble_global_stiffness_matrix()
        actual = truss_structure.transformation_matrix(np.radians(38.66))
        nte.assert_allclose(actual,np.array([
    [0.78087, -0.6247, 0,       0],
    [0.6247,   0.78087, 0,       0],
    [0,        0,       0.78087, -0.6247],
    [0,        0,       0.6247,  0.78087]
                                            ]))

    def test_transformed_local_matrix(self,
                                      truss_structure):
        truss_structure.assemble_global_stiffness_matrix()
        actual = truss_structure.transformed_local_matrix
        nte.assert_allclose(actual,
                            np.array([
    [ 2.67e3,  2.13e3, -2.67e3, -2.13e3],
    [ 2.13e3,  1.71e3, -2.13e3, -1.71e3],
    [-2.67e3, -2.13e3,  2.67e3,  2.13e3],
    [-2.13e3, -1.71e3,  2.13e3,  1.71e3]
])                       
                            )

