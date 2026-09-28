import numpy as np

from elements import Element
from solver import displacement
from global_stiffness import TrussStructure.

def reaction():
    return GSM @ displacement - forces

def strain(node_matrix, displacement):
    strain = np.array(np.zeros(node_matrix.shape[0]/4))
    for i in range(node_matrix.shape[0]/4):
        strain.append[i] = displacement[i] / Element.length
    return strain

def stress(element_list, node_matrix):
    stress = np.array(np.zeros(node_matrix.shape[0]/4))
    for i in range(node_matrix.shape[0]/4):
        stress.append[i] = element_list[i.E] * strain[i]

    return stress