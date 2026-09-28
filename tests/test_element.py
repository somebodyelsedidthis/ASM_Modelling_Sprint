from elements import Element
import numpy as np

NODE_I = [0, 0]
NODE_J = [3, 4]
E = 200.0
A = 2.0
I = 10.0
RHO = 1.0


def test_element():
    # If Pythagoras didn't lie this should pass
    elem = Element(NODE_I, NODE_J, E, A, I, RHO, "truss")
    assert np.isclose(elem.length([NODE_I, NODE_J]), 5.0)
    # The truss matrix should be a symmetric 2x2 matrix
    k_truss = elem.stiffness_matrix()
    assert k_truss.shape == (2, 2)
    assert np.allclose(k_truss, k_truss.T)

    # The beam matrix should also be a symmetric 6x6 matrix
    elem_beam = Element(NODE_I, NODE_J, E, A, I, RHO, "frame")
    k_beam = elem_beam.stiffness_matrix()
    assert k_beam.shape == (6, 6)
    assert np.allclose(k_beam, k_beam.T)

    print("All passed")


if __name__ == "__main__":
    test_element()