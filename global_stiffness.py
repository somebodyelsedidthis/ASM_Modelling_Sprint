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
        print('Nodes: ',nodes)
        print(nodes.shape)
        self.elements = elements
        self.angles = angles
        self.total_DOFs = len(list(nodes))*2
        self.connectivity_matrix = connectivity_matrix

    def _transformation_matrix(self,
                               theta_rad: float):
        return np.array([
            [np.cos(theta_rad), -np.sin(theta_rad), 0.0, 0.0],
            [np.sin(theta_rad), np.cos(theta_rad), 0.0, 0.0],
            [0.0, 0.0, np.cos(theta_rad), -np.sin(theta_rad)],
            [0.0, 0.0, np.sin(theta_rad), np.cos(theta_rad)]
        ])

    def _boolean_connectivity_matrix(self,
                                     node1: int,
                                     node2: int):
        L_e = np.zeros((4, self.total_DOFs))
        L_e[0, 2*node1] = 1.0  # Local row 0 -> Node A (x)
        L_e[1, 2*node1+1] = 1.0  # Local row 1 -> Node A (y)
        L_e[2, 2*node2] = 1.0  # Local row 2 -> Node B (x)
        L_e[3, 2*node2+1] = 1.0  # Local row 3 -> Node B (y)

        return L_e

    def assemble_global_stiffness_matrix(self):
        self.global_stiffness_matrix = np.zeros((self.total_DOFs,self.total_DOFs))
    
        for i in range(len(self.elements)):
            rotation_angle = self.angles[i]
            node1=self.connectivity_matrix[i][0]
            node2=self.connectivity_matrix[i][1]

            self.transformation_matrix = self._transformation_matrix(rotation_angle)
            local_stiffness_matrix = self.elements[i].local_stiffness_matrix
            self.transformed_local_matrix = (self.transformation_matrix@local_stiffness_matrix)@np.linalg.inv(self.transformation_matrix)                          
            
            boolean_connectivity_matrix = self._boolean_connectivity_matrix(node1,
                                                                            node2)
            
            self.global_stiffness_matrix+=np.transpose(boolean_connectivity_matrix)@self.transformed_local_matrix@boolean_connectivity_matrix

        return self.global_stiffness_matrix

        
