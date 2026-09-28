import numpy as np

from post_proc import reaction, strain, stress
from nodes import Node
from elements import Element
from global_stiffness import TrussStructure


def test_reaction():
    """
    Test reaction forces using the same simple system as test_solver.py.

    Expected:
    - Applied force of +10 at DOF 2
    - Reaction force of -10 at constrained DOF 0
    """

    K = np.array([
        [10.0, -10.0, 0.0],
        [-10.0, 20.0, -10.0],
        [0.0, -10.0, 10.0]
    ])

    displacement = np.array([
        0.0,
        1.0,
        2.0
    ])

    forces = np.array([
        0.0,
        0.0,
        10.0
    ])

    reactions = reaction(K, displacement, forces)

    expected_reactions = np.array([
        -10.0,
        0.0,
        0.0
    ])

    assert np.allclose(reactions, expected_reactions)


def test_strain():
    """
    Test strain for a diagonal truss element.

    Element:
        Node 0 = (0, 0)
        Node 1 = (3, 4)

    Therefore:
        Length = 5

    Node 1 moves 0.006 in x and 0.008 in y.
    This displacement is exactly 0.01 along the element axis.

    Expected strain:
        0.01 / 5 = 0.002
    """

    node_list = np.array([
        Node(0.0, 0.0),
        Node(3.0, 4.0)
    ], dtype=object)

    element_list = [
        Element(
            node_i=0,
            node_j=1,
            E=200e9,
            A=0.01
        )
    ]

    connectivity_matrix = np.array([
        [0, 1]
    ])

    angles = np.array([
        np.arctan2(4.0, 3.0)
    ])

    displacement = np.array([
        0.0, 0.0,       # Node 0: ux, uy
        0.006, 0.008    # Node 1: ux, uy
    ])

    structure = TrussStructure(
        element_list,
        node_list,
        connectivity_matrix,
        angles
    )

    strains = strain(
        element_list,
        node_list,
        connectivity_matrix,
        displacement,
        angles,
        structure
    )

    expected_strains = np.array([
        0.002
    ])

    assert np.allclose(strains, expected_strains)


def test_stress():
    """
    Test stress = E * strain for two elements.

    First element is in tension.
    Second element is in compression.
    """

    element_list = [
        Element(
            node_i=0,
            node_j=1,
            E=200e9,
            A=0.01
        ),
        Element(
            node_i=1,
            node_j=2,
            E=70e9,
            A=0.01
        )
    ]

    strains = np.array([
        0.001,
        -0.002
    ])

    stresses = stress(element_list, strains)

    expected_stresses = np.array([
        200e6,
        -140e6
    ])

    assert np.allclose(stresses, expected_stresses)