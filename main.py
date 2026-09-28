import elements
import rotation
import nodes
import global_stiffness
import solver
import post_proc

import numpy as np

def main(node_info, element_info):

    node_list = nodes.create_nodes(node_info)
    element_list = nodes.create_elements(element_info)
    connectivity_matrix = nodes.connectivity(element_list)
    forces = nodes.force_matrix(node_list)
    
    pass