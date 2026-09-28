import numpy as np
from nodes import Node
from elements import Element
from rotation import rotation_angles


def test_rotation_angles():

    # Create nodes
    node_list = [
        Node(0.0, 0.0),
        Node(1.0, 0.0),
        Node(1.0, 1.0),
        Node(0.0, 1.0)
    ]

    # Create elements using node indices
    elements = [
        Element(
            node_i=0,
            node_j=1,
            E=70e9,
            A=0.01
        ),

        Element(
            node_i=0,
            node_j=2,
            E=70e9,
            A=0.01
        ),

        Element(
            node_i=0,
            node_j=3,
            E=70e9,
            A=0.01
        )
    ]

    # Calculate rotation angles
    angles = rotation_angles(elements, node_list)

    # Expected angles
    expected = np.array([
        0.0,
        np.pi / 4,
        np.pi / 2
    ])

    # Compare calculated and expected values
    np.testing.assert_allclose(angles, expected)