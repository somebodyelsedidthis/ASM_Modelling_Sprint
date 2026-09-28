import numpy as np
from elements import Element

class TrussStructure:
    def __init__(self,
                 elements: Element[np.ndarray],
                 angles: np.ndarray,
                 ):
        self.elements = elements
        self.angles = angles
        self.local_matrices = []
        self.transformed_local_matrices = []
        for i in elements:
            #the method has to be changed to modify the element attributes
            self.local_matrices.append(self.elements.stiffness_matrix)


    def _transformation_matrix(self, theta_rad: float):
        return np.array([
            [np.cos(theta_rad), -np.sin(theta_rad), 0.0, 0.0],
            [np.sin(theta_rad), np.cos(theta_rad), 0.0, 0.0],
            [0.0, 0.0, np.cos(theta_rad), -np.sin(theta_rad)],
            [0.0, 0.0, np.sin(theta_rad), np.cos(theta_rad)]
        ])


    def assemble_global_stiffness_matrix(self):
        for i in range(len(self.local_matrices)):
            rotation_angle = self.angles[i]
            local_stiffness_matrix = self.local_matrices[i]
            transformation_matrix = self._transformation_matrix(self, rotation_angle)
            transformed_local_matrix = (transformation_matrix@local_stiffness_matrix)@np.linalg.inv(transformation_matrix)                          
            self.transformed_local_matrices.append(transformed_local_matrix)
        
        self.global_stiffness_matrix = np.block_diag(self.transformed_local_matrices)