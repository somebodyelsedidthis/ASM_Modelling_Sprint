import numpy as np
import math

def rotation_angles(elements):
#Calculate the rotation angle with respect to global x axis in radians
    angles = []
    for element in elements:
        dx, dy = element.node_j - element.node_i
        theta = np.arctan2(dy, dx)
        angles.append(theta)

    return np.array(angles)
