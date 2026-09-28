import numpy as np

class Element:
    def __init__(self, node_i, node_j, E, A, I=1.0, rho=1.0, element_type="truss"):
        self.node_i = np.asarray(node_i)
        self.node_j = np.asarray(node_j)
        self.E = E
        self.A = A # This is the cross-sectional area regardless of beam shape
        self.I = I
        self.rho = rho
        self.element_type = element_type

    def length(self):
        return np.linalg.norm(self.node_j - self.node_i)

    def angle(self):
        # This is the angle from the horizontal in the counter-clockwise direction (-pi to pi)
        # it is not used here, but it will be useful for the rotation matrix
        dx, dy = self.node_j - self.node_i
        return np.arctan2(dy, dx)

    def stiffness_matrix(self):
        L = self.length()
        E = self.E
        A = self.A
        I = self.I

        if self.element_type == "truss":
            return (E * A / L) * np.array([
                [1.0, -1.0],
                [-1.0, 1.0]
            ])

        elif self.element_type == "frame": # Someone please check this I think I have it correct but you never know
            return np.array([
                [E * A / L, 0.0, 0.0, -E * A / L, 0.0, 0.0],
                [0.0, 12.0 * E * I / L ** 3, 6.0 * E * I / L ** 2,
                 0.0, -12.0 * E * I / L ** 3, 6.0 * E * I / L ** 2],
                [0.0, 6.0 * E * I / L ** 2, 4.0 * E * I / L,
                 0.0, -6.0 * E * I / L ** 2, 2.0 * E * I / L],
                [-E * A / L, 0.0, 0.0, E * A / L, 0.0, 0.0],
                [0.0, -12.0 * E * I / L ** 3, -6.0 * E * I / L ** 2,
                 0.0, 12.0 * E * I / L ** 3, -6.0 * E * I / L ** 2],
                [0.0, 6.0 * E * I / L ** 2, 2.0 * E * I / L,
                 0.0, -6.0 * E * I / L ** 2, 4.0 * E * I / L]
            ])
    # I didn't implement mass matrix but if we want to implement gravity loads like that I can do that too