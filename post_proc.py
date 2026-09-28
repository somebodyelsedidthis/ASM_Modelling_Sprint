import numpy as np

from elements import Element
from solver import Solver
from global_stiffness import 

def reaction():
    return GSM @ Solver.displacement - forces

def strain(node_matrix, Solver.displacement):
    strain = np.array(np.zeros(node_matrix.shape[0]/4))
    for i in range(node_matrix.shape[0]/4):
        strain.append[i] = Solver.displacement[i] / Element.length
    return strain

def stress(element_list, node_matrix):
    stress = np.array(np.zeros(node_matrix.shape[0]/4))
    for i in range(node_matrix.shape[0]/4):
        stress.append[i] = element_list[i.E] * strain[i]

    return stress