import numpy as np
from nodes import Node

class Element:
    def __init__(self,
                 node_i: int,
                 node_j: int,
                 E: float,
                 A: float,
                 I: float = 1.0,
                 rho: float = 1.0,
                 element_type: str="truss"):
        
        self.node_i = np.asarray(node_i)
        self.node_j = np.asarray(node_j)
        self.E = E
        self.A = A # This is the cross-sectional area regardless of beam shape
        self.I = I
        self.rho = rho
        self.element_type = element_type

    def length(self, node_list):
        ni = node_list[self.node_i]
        nj = node_list[self.node_j]
        self.element_length = np.linalg.norm(nj.coords - ni.coords)
        return self.element_length

    def stiffness_matrix(self, node_list):
        L = self.length(node_list)
        E = self.E
        A = self.A
        I = self.I

        if self.element_type == "truss":
            self.local_stiffness_matrix = (E * A / L) * np.array([
                [1.0, 0, -1.0, 0],
                [0,0,0,0],
                [-1.0, 0, 1.0, 0],
                [0,0,0,0]
            ])

        elif self.element_type == "frame": # Someone please check this I think I have it correct but you never know
            self.local_stiffness_matrix = np.array([
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

        else:
            raise ValueError(f'Unsupported element type: {self.element_type}')

        return self.local_stiffness_matrix
    # I didn't implement mass matrix but if we want to implement gravity loads like that I can do that too