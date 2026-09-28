import numpy as np
import pytest
import numpy.testing as nte
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from global_stiffness import TrussStructure
from nodes import create_nodes, create_elements


K_ELEM_1 = np.array([
    [ 2.6664e6,  2.1331e6, -2.6664e6, -2.1331e6],
    [ 2.1331e6,  1.7065e6, -2.1331e6, -1.7065e6],
    [-2.6664e6, -2.1331e6,  2.6664e6,  2.1331e6],
    [-2.1331e6, -1.7065e6,  2.1331e6,  1.7065e6],
])

K_ELEM_0 = 5.6e6 * np.array([
    [ 1.0, 0.0, -1.0, 0.0],
    [ 0.0, 0.0,  0.0, 0.0],
    [-1.0, 0.0,  1.0, 0.0],
    [ 0.0, 0.0,  0.0, 0.0],
])


@pytest.fixture
def elements():
    element_info = [{'node_i': 1,
                     'node_j': 2,
                     'E': 70e9,
                     'A': 10e-6},
                    {'node_i': 0,
                     'node_j': 1,
                     'E': 70e9,
                     'A': 10e-6}]
    return create_elements(element_info=element_info)


@pytest.fixture
def nodes():
    node_info = [{'x': 0.0,
                  'y': 0.0,
                  'C_x': True,
                  'C_y': True},
                 {'x': 125.0 / 1000,
                  'y': 100.0 / 1000,
                  'C_x': False,
                  'C_y': False},
                 {'x': 0.0,
                  'y': 100.0 / 1000,
                  'C_x': True,
                  'C_y': True}]
    return create_nodes(node_info=node_info)


@pytest.fixture
def connectivity_matrix():
    return np.array([
        [1, 2],
        [0, 1],
    ])


@pytest.fixture
def angles():
    return np.array([
        np.arctan2(0.0, -0.125),
        np.arctan2(0.1, 0.125),
    ])


@pytest.fixture
def truss_structure(elements, nodes, connectivity_matrix, angles):
    return TrussStructure(np.array(elements),
                          np.array(nodes),
                          np.array(connectivity_matrix),
                          np.array(angles))


class TestTransformationMatrix:
    def test_transformation_matrix(self, truss_structure):
        actual = truss_structure._transformation_matrix(np.radians(38.66))
        expected = np.array([
            [0.78087, -0.6247, 0.0,      0.0],
            [0.6247,   0.78087, 0.0,      0.0],
            [0.0,      0.0,     0.78087, -0.6247],
            [0.0,      0.0,     0.6247,   0.78087],
        ])
        nte.assert_allclose(actual, expected, rtol=1e-3, atol=1e-5)

    def test_zero_angle_is_identity(self, truss_structure):
        nte.assert_allclose(truss_structure._transformation_matrix(0.0),
                            np.eye(4), atol=1e-12)

    def test_transformation_matrix_is_orthogonal(self, truss_structure):
        T = truss_structure._transformation_matrix(np.radians(38.66))
        nte.assert_allclose(T @ T.T, np.eye(4), atol=1e-12)


class TestElementGlobalMatrix:
    def test_inclined_element(self, truss_structure):
        actual = truss_structure.element_global_matrix(1)
        nte.assert_allclose(actual, K_ELEM_1, rtol=1e-3)

    def test_horizontal_element(self, truss_structure):
        actual = truss_structure.element_global_matrix(0)
        nte.assert_allclose(actual, K_ELEM_0, rtol=1e-3, atol=1e-3)


class TestGlobalStiffness:
    def test_shape(self, truss_structure):
        K = truss_structure.assemble_global_stiffness_matrix()
        assert K.shape == (6, 6)

    def test_assembled_values(self, truss_structure):
        K = truss_structure.assemble_global_stiffness_matrix()
        expected = np.zeros((6, 6))
        expected[0:4, 0:4] += K_ELEM_1
        expected[2:6, 2:6] += K_ELEM_0
        nte.assert_allclose(K, expected, rtol=1e-3, atol=1e-3)

    def test_symmetric(self, truss_structure):
        K = truss_structure.assemble_global_stiffness_matrix()
        nte.assert_allclose(K, K.T, rtol=1e-12, atol=1e-6)
