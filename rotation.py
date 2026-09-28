import numpy as np
import math

# def rotation_angles(elements):
# #Calculate the rotation angle with respect to global x axis in radians
#     angles = []
#     for element in elements:
#         dx, dy = element.node_j - element.node_i
#         theta = np.arctan2(dy, dx)
#         angles.append(theta)

#     return np.array(angles)

def rotation_angles(elements, node_list):
    angles = []

    for element in elements:
        node_i = node_list[element.node_i]
        node_j = node_list[element.node_j]

        dx = node_j.x - node_i.x
        dy = node_j.y - node_i.y

        angles.append(np.arctan2(dy, dx))

    return np.array(angles)
