import numpy as np

def boolean_connectivity_matrix(node1: int,
                                node2: int):

    total_DOFs=6    
    L_e = np.zeros((4, total_DOFs))
    L_e[0, 2*node1] = 1.0  # Local row 0 -> Node A (x)
    L_e[1, 2*node1+1] = 1.0  # Local row 1 -> Node A (y)
    L_e[2, 2*node2] = 1.0  # Local row 2 -> Node B (x)
    L_e[3, 2*node2+1] = 1.0  # Local row 3 -> Node B (y)

    return L_e


def transformation_matrix(theta_rad: float):
        return np.array([
            [np.cos(theta_rad), -np.sin(theta_rad), 0.0, 0.0],
            [np.sin(theta_rad), np.cos(theta_rad), 0.0, 0.0],
            [0.0, 0.0, np.cos(theta_rad), -np.sin(theta_rad)],
            [0.0, 0.0, np.sin(theta_rad), np.cos(theta_rad)]
        ])

transformed_local_matrix= np.array([
    [ 2.67e3,  2.13e3, -2.67e3, -2.13e3],
    [ 2.13e3,  1.71e3, -2.13e3, -1.71e3],
    [-2.67e3, -2.13e3,  2.67e3,  2.13e3],
    [-2.13e3, -1.71e3,  2.13e3,  1.71e3]
])                       

boolean_matrix = boolean_connectivity_matrix(0,1)
print('Boolean matrix: ',boolean_matrix)
global_stiffness_matrix=np.zeros((6,6),dtype=np.float64)
print('Global stiffness matrix: ',global_stiffness_matrix)
global_stiffness_matrix+=(np.transpose(boolean_matrix)@transformed_local_matrix)@boolean_matrix
print(global_stiffness_matrix)