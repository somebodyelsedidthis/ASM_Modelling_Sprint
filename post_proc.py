import numpy as np

from elements import Element
from solver import Solver
from global_stiffness import TrussStructure

# def reaction(TrussStructure.assemble_global_stiffness_matrix, Solver.displacement):
#     GSM = TrussStructure.assemble_global_stiffness_matrix
#     u = Solver.displacement
#     return GSM @ u - forces

def reaction(global_stiffness_matrix, displacement, forces):

    displacement = np.asarray(displacement).reshape(-1)
    forces = np.asarray(forces).reshape(-1)

    return global_stiffness_matrix @ displacement - forces

# def strain(node_matrix, Solver.displacement):
#     strain = np.array(np.zeros(node_matrix.shape[0]/4))
#     for i in range(node_matrix.shape[0]/4):
#         strain.append[i] = Solver.displacement[i] / Element.length
#     return strain

def strain(element_list, node_list, connectivity_matrix,
           displacement, angles, TrussStructure):

    strains = np.zeros(len(element_list))

    for i in range(len(element_list)):

        node_i = connectivity_matrix[i][0]
        node_j = connectivity_matrix[i][1]

        # Displacements of this element in global coordinates
        u_global = np.array([
            displacement[2 * node_i],
            displacement[2 * node_i + 1],
            displacement[2 * node_j],
            displacement[2 * node_j + 1]
        ])

        # Same 4x4 transformation matrix used for stiffness
        T = TrussStructure._transformation_matrix(angles[i])

        # Global -> local displacement
        u_local = T.T @ u_global

        L = element_list[i].length(node_list)

        # Difference in LOCAL AXIAL displacement
        strains[i] = (u_local[2] - u_local[0]) / L

    return strains

# def stress(element_list, node_matrix):
#     stress = np.array(np.zeros(node_matrix.shape[0]/4))
#     for i in range(node_matrix.shape[0]/4):
#         stress.append[i] = element_list[i.E] * strain[i]

#     return stress

def stress(element_list, strains):

    stresses = np.zeros(len(element_list))

    for i in range(len(element_list)):
        stresses[i] = element_list[i].E * strains[i]

    return stresses