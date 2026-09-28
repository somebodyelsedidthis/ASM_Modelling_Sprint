import elements
import rotation
import nodes
import numpy as np

def main(element_info):
    element_list = nodes.create_elements(element_info)
    connectivity_matrix, node_matrix = nodes.information(element_list)
    angles = rotation.rotation_angles(element_list)



    pass