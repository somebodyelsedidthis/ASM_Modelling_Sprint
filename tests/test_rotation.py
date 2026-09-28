import numpy as np
from elements import Element
from rotation import rotation_angles


def test_rotation_angles():
    elements = [
        Element(
            node_i=np.array([0.0, 0.0]),
            node_j=np.array([1.0, 0.0]),
            E=70e9,
            A=0.01
        ),

        Element(
            node_i=np.array([0.0, 0.0]),
            node_j=np.array([1.0, 1.0]),
            E=70e9,
            A=0.01
        ),

        Element(
            node_i=np.array([0.0, 0.0]),
            node_j=np.array([0.0, 1.0]),
            E=70e9,
            A=0.01
        )
    ]

    angles = rotation_angles(elements)

    expected = np.array([
        0.0,
        np.pi / 4,
        np.pi / 2
    ])

    np.testing.assert_allclose(angles, expected)