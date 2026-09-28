import numpy as np

from elements import length, stiffness_matrix
from solver import displacement
from Global_SM import GSM
from main import forces, element_list

class post_proc:
    def reaction():
        return GSM @ displacement - forces

    def strain():
        return e

    def stress():
        stress = np.array(np.zeros(len(nodes)/4))
        for i in range(len(nodes)/4):
            stress.append[i] = element_list[i.E] * strain[i]

        return stress