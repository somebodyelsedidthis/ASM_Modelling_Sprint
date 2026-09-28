import numpy as np
from elements import Element
from nodes import Node


class TrussStructure:
    def __init__(self,
                 elements: np.ndarray[Element],
                 nodes: np.ndarray[Node],
                 connectivity_matrix: np.ndarray[int],
                 angles: np.ndarray[float],
                 ):

        self.elements = elements
        self.angles = angles
        self.total_DOFs = len(nodes) * 2
        self.connectivity_matrix = connectivity_matrix
        self.nodes = nodes

    @staticmethod
    def _transformation_matrix(theta_rad: float):
        c, s = np.cos(theta_rad), np.sin(theta_rad)
        R = np.array([[c, -s],
                      [s,  c]])
        T = np.zeros((4, 4))
        T[:2, :2] = R
        T[2:, 2:] = R
        return T

    def element_global_matrix(self, i: int):
        T = self._transformation_matrix(self.angles[i])
        k_local = self.elements[i].stiffness_matrix(self.nodes)
        return T @ k_local @ T.T

    def assemble_global_stiffness_matrix(self):
        K = np.zeros((self.total_DOFs, self.total_DOFs))

        for i, (node1, node2) in enumerate(self.connectivity_matrix):
            node1, node2 = int(node1), int(node2)
            dofs = [2 * node1, 2 * node1 + 1, 2 * node2, 2 * node2 + 1]
            K[np.ix_(dofs, dofs)] += self.element_global_matrix(i)

        self.global_stiffness_matrix = K
        return K